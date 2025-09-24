# Gobernanza de Datos

Lineamientos de este laboratorio:

- **Bronze**: datos crudos tal como llegan, con trazabilidad de archivo.
- **Silver**: datos validados y normalizados para análisis.
- **Gold**: métricas y KPIs listos para visualización.
- **Trazabilidad**: incluir `__source_file`, `__ingest_ts`, `__commit_hash` en las tablas.
- **No subir datos sensibles** al repositorio.
