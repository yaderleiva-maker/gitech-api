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
            # 1. Verificar si el producto ya existe
            query_verificar = f"""
                SELECT id_externo FROM `{config.PROJECT_ID}.{config.DATASET_ID}.productos`
                WHERE id_externo = @id_externo
            """
            df_existente = BigQueryClient.execute_query_safe(
                query_verificar,
                id_externo=producto_data.id_externo
            )
            
            # 2. Calcular existencia
            existencia = producto_data.total_compras - producto_data.total_ventas
            
            if df_existente.empty:
                # 3a. INSERTAR
                # Obtener el último id_producto para asignar el siguiente
                query_max_id = f"""
                    SELECT COALESCE(MAX(id_producto), 0) + 1 AS next_id
                    FROM `{config.PROJECT_ID}.{config.DATASET_ID}.productos`
                """
                df_max_id = BigQueryClient.execute_query(query_max_id)
                next_id = df_max_id['next_id'].values[0]
                
                query_insert = f"""
                    INSERT INTO `{config.PROJECT_ID}.{config.DATASET_ID}.productos` (
                        id_producto, id_externo, nombre_prod, descripcion, precio_base, 
                        activo, min_stock, categoria, marca, modelo, foto,
                        total_compras, total_ventas, existencia,
                        fecha_creacion, fecha_actualizacion
                    ) VALUES (
                        @id_producto, @id_externo, @nombre, @descripcion, @precio_base,
                        @activo, @min_stock, @categoria, @marca, @modelo, @foto,
                        @total_compras, @total_ventas, @existencia,
                        CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()
                    )
                """
                BigQueryClient.execute_query_safe(
                    query_insert,
                    id_producto=next_id,
                    id_externo=producto_data.id_externo,
                    nombre=producto_data.nombre_prod,
                    descripcion=producto_data.descripcion,
                    precio_base=producto_data.precio_base,
                    activo=producto_data.activo,
                    min_stock=producto_data.min_stock,
                    categoria=producto_data.categoria,
                    marca=producto_data.marca,
                    modelo=producto_data.modelo,
                    foto=producto_data.foto,
                    total_compras=producto_data.total_compras,
                    total_ventas=producto_data.total_ventas,
                    existencia=existencia
                )
                accion = "INSERTADO"
                id_producto = next_id
                
            else:
                # 3b. ACTUALIZAR
                query_update = f"""
                    UPDATE `{config.PROJECT_ID}.{config.DATASET_ID}.productos`
                    SET 
                        nombre_prod = @nombre,
                        descripcion = @descripcion,
                        precio_base = @precio_base,
                        activo = @activo,
                        min_stock = @min_stock,
                        categoria = @categoria,
                        marca = @marca,
                        modelo = @modelo,
                        foto = @foto,
                        total_compras = @total_compras,
                        total_ventas = @total_ventas,
                        existencia = @existencia,
                        fecha_actualizacion = CURRENT_TIMESTAMP()
                    WHERE id_externo = @id_externo
                """
                BigQueryClient.execute_query_safe(
                    query_update,
                    id_externo=producto_data.id_externo,
                    nombre=producto_data.nombre_prod,
                    descripcion=producto_data.descripcion,
                    precio_base=producto_data.precio_base,
                    activo=producto_data.activo,
                    min_stock=producto_data.min_stock,
                    categoria=producto_data.categoria,
                    marca=producto_data.marca,
                    modelo=producto_data.modelo,
                    foto=producto_data.foto,
                    total_compras=producto_data.total_compras,
                    total_ventas=producto_data.total_ventas,
                    existencia=existencia
                )
                accion = "ACTUALIZADO"
                
                # Obtener el id_producto existente
                id_producto = df_existente.iloc[0]['id_externo']
            
            logger.info(f"Producto {accion}: ID externo {producto_data.id_externo}")
            
            return {
                "status": "success",
                "accion": accion,
                "id_externo": producto_data.id_externo,
                "id_producto": id_producto,
                "existencia": existencia,
                "mensaje": f"Producto {accion} correctamente"
            }
            
        except Exception as e:
            logger.error(f"Error al procesar producto: {e}")
            raise Exception(f"Error al guardar producto: {str(e)}")
