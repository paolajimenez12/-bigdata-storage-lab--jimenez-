# 🛡️ Gobernanza de Datos

Este laboratorio implementa lineamientos básicos de **gobierno de datos** para garantizar confiabilidad, trazabilidad y seguridad.

---

## 🔗 Origen y Linaje

- **Bronze**: datos crudos tal como llegan, con metadatos (`__source_file`, `__ingest_ts`, `__file_md5`).  
- **Silver**: datos normalizados bajo el esquema canónico (`date`, `partner`, `amount`).  
- **Gold**: métricas y KPIs derivados de la capa Silver.  
- Cada transformación incluye referencias al commit de código (`__commit_hash`) y timestamp (`__transformation_ts`).

---

## ✅ Validaciones mínimas

1. **Presencia de columnas requeridas**: `date`, `partner`, `amount`.  
2. **Tipos consistentes**:  
   - `date` → formato ISO (`YYYY-MM-DD`).  
   - `partner` → cadena de texto no vacía.  
   - `amount` → numérico, no negativo.  
3. **Reglas de negocio**:  
   - `amount >= 0`.  
   - `date` no debe ser futura.  
4. **Duplicados**: eliminación o marcaje de filas duplicadas por (`date`, `partner`, `amount`).

---

## 🔒 Política de mínimos privilegios

- Acceso **lectura/escritura** limitado a roles técnicos responsables de ingesta y procesamiento.  
- Acceso **solo lectura** a la capa Silver y Gold para analistas y visualizadores.  
- No se comparten credenciales en repositorios ni scripts.  
- Se aplican `.gitignore` y `.gitkeep` para controlar visibilidad de datos.

---

## 🧾 Trazabilidad

- Cada dataset incluye metadatos obligatorios:  
  - `__source_file`, `__ingest_ts`, `__file_md5`.  
  - `__transformation_ts`, `__commit_hash`.  
- Se mantiene un **manifest** con historial de ingesta y validación por archivo.  
- Validaciones generan reportes JSON accesibles para auditoría.  

---

## 👥 Roles

| Rol              | Responsabilidad principal                                |
|------------------|----------------------------------------------------------|
| **Ingestor**     | Configurar la ingesta, registrar archivos en Bronze.      |
| **Validador**    | Definir y aplicar reglas de calidad.                      |
| **Transformador**| Implementar normalización y generar capa Silver.          |
| **Analista**     | Consumir Silver/Gold y diseñar KPIs en Streamlit.         |
| **Auditor**      | Revisar linaje, trazabilidad y cumplimiento de reglas.    |
