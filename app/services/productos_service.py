from app.database.bigquery import BigQueryClient
from app.config import config
from app.models.productos import ProductoInput
import logging

logger = logging.getLogger(__name__)

class ProductosService:
    
    @staticmethod
    def upsert_producto(producto_data: ProductoInput) -> dict:
        """Inserta o actualiza un producto en BigQuery."""
        try:
            # 🔍 Validar que el SKU no esté duplicado
            query_verificar_codigo = f"""
                SELECT id_producto 
                FROM `{config.PROJECT_ID}.{config.DATASET_ID}.productos`
                WHERE codigo = @codigo AND id_externo != @id_externo
            """
            df_codigo_existente = BigQueryClient.execute_query_safe(
                query_verificar_codigo,
                codigo=producto_data.codigo,
                id_externo=producto_data.id_externo
            )
            
            if not df_codigo_existente.empty:
                raise Exception(f"El SKU '{producto_data.codigo}' ya está asignado a otro producto")
            
            # 🔍 Validar que el código de barras no esté duplicado
            if producto_data.codigo_barras:
                query_verificar_barras = f"""
                    SELECT id_producto 
                    FROM `{config.PROJECT_ID}.{config.DATASET_ID}.productos`
                    WHERE codigo_barras = @codigo_barras AND id_externo != @id_externo
                """
                df_barras_existente = BigQueryClient.execute_query_safe(
                    query_verificar_barras,
                    codigo_barras=producto_data.codigo_barras,
                    id_externo=producto_data.id_externo
                )
                
                if not df_barras_existente.empty:
                    raise Exception(f"El código de barras '{producto_data.codigo_barras}' ya está asignado a otro producto")
            
            # 🔍 Verificar si el producto ya existe por id_externo
            query_verificar = f"""
                SELECT id_producto 
                FROM `{config.PROJECT_ID}.{config.DATASET_ID}.productos`
                WHERE id_externo = @id_externo
            """
            df_existente = BigQueryClient.execute_query_safe(
                query_verificar,
                id_externo=producto_data.id_externo
            )
            
            if df_existente.empty:
                # ➕ INSERTAR: Obtener siguiente ID con REGEXP_EXTRACT
                query_max_id = f"""
                    SELECT COALESCE(
                        MAX(SAFE_CAST(REGEXP_EXTRACT(id_producto, r'GIT-PROD-(\\d+)') AS INT64)),
                        0
                    ) + 1 AS next_id
                    FROM `{config.PROJECT_ID}.{config.DATASET_ID}.productos`
                """
                df_max_id = BigQueryClient.execute_query(query_max_id)
                next_id = int(df_max_id.iloc[0]["next_id"])
                
                # 🔥 Generar ID en formato STRING
                id_producto = f"GIT-PROD-{str(next_id).zfill(6)}"
                
                query_insert = f"""
                    INSERT INTO `{config.PROJECT_ID}.{config.DATASET_ID}.productos` (
                        id_producto, id_externo, codigo, codigo_barras, 
                        nombre, descripcion, categoria, marca, modelo,
                        precio_base, activo, stock_minimo, foto,
                        fecha_creacion, fecha_actualizacion
                    ) VALUES (
                        @id_producto, @id_externo, @codigo, @codigo_barras,
                        @nombre, @descripcion, @categoria, @marca, @modelo,
                        @precio_base, @activo, @stock_minimo, @foto,
                        CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()
                    )
                """
                BigQueryClient.execute_query_safe(
                    query_insert,
                    id_producto=id_producto,
                    id_externo=producto_data.id_externo,
                    codigo=producto_data.codigo,
                    codigo_barras=producto_data.codigo_barras,
                    nombre=producto_data.nombre,
                    descripcion=producto_data.descripcion,
                    categoria=producto_data.categoria,
                    marca=producto_data.marca,
                    modelo=producto_data.modelo,
                    precio_base=producto_data.precio_base,
                    activo=producto_data.activo,
                    stock_minimo=producto_data.stock_minimo,
                    foto=producto_data.foto
                )
                accion = "INSERTADO"
                
            else:
                # 🔄 ACTUALIZAR
                id_producto = df_existente.iloc[0]["id_producto"]
                
                query_update = f"""
                    UPDATE `{config.PROJECT_ID}.{config.DATASET_ID}.productos`
                    SET 
                        codigo = @codigo,
                        codigo_barras = @codigo_barras,
                        nombre = @nombre,
                        descripcion = @descripcion,
                        categoria = @categoria,
                        marca = @marca,
                        modelo = @modelo,
                        precio_base = @precio_base,
                        activo = @activo,
                        stock_minimo = @stock_minimo,
                        foto = @foto,
                        fecha_actualizacion = CURRENT_TIMESTAMP()
                    WHERE id_producto = @id_producto
                """
                BigQueryClient.execute_query_safe(
                    query_update,
                    id_producto=id_producto,
                    codigo=producto_data.codigo,
                    codigo_barras=producto_data.codigo_barras,
                    nombre=producto_data.nombre,
                    descripcion=producto_data.descripcion,
                    categoria=producto_data.categoria,
                    marca=producto_data.marca,
                    modelo=producto_data.modelo,
                    precio_base=producto_data.precio_base,
                    activo=producto_data.activo,
                    stock_minimo=producto_data.stock_minimo,
                    foto=producto_data.foto
                )
                accion = "ACTUALIZADO"
            
            logger.info(f"Producto {accion}: SKU {producto_data.codigo}, ID externo {producto_data.id_externo}")
            
            return {
                "status": "success",
                "accion": accion,
                "id_externo": producto_data.id_externo,
                "id_producto": id_producto,
                "codigo": producto_data.codigo,
                "mensaje": f"Producto {accion} correctamente"
            }
            
        except Exception as e:
            logger.error(f"Error al procesar producto: {e}")
            raise Exception(f"Error al guardar producto: {str(e)}")