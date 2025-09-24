# 📘 Diccionario de Datos - Esquema Canónico

El esquema canónico define cómo se normalizan los datos en la **capa Silver** del laboratorio.  
Los campos están tipificados y alineados con las mejores prácticas de gobierno de datos.

---

## 📐 Esquema Canónico

| Campo   | Tipo     | Formato / Unidad | Descripción                              |
|---------|----------|------------------|------------------------------------------|
| date    | date     | YYYY-MM-DD       | Fecha del evento transaccional.           |
| partner | string   | texto plano      | Nombre o identificador del socio/cliente. |
| amount  | float    | EUR              | Importe numérico en euros.                |

---

## 🔄 Mapeos de columnas de origen → canónico

Ejemplos típicos de cómo normalizar distintas denominaciones de campos:

| Origen (columna) | Canónico | Notas de transformación                     |
|------------------|----------|---------------------------------------------|
| `Fecha`          | date     | Convertir a formato ISO `YYYY-MM-DD`.       |
| `partner_name`   | partner  | Limpiar espacios, aplicar `lower()`.        |
| `cliente`        | partner  | Mapear al campo `partner`.                  |
| `importe`        | amount   | Convertir a `float` en EUR.                 |
| `monto_total`    | amount   | Normalizar unidad monetaria a EUR.          |
| `transaction_dt` | date     | Parsear timestamp y truncar a fecha.        |

---

## 📌 Notas

- Todos los campos **deben ser no nulos** en la capa Silver.  
- Los valores de `partner` se normalizan en minúsculas y sin caracteres especiales cuando sea posible.  
- `amount` se almacena siempre en **euros** (EUR), aplicando conversión si el dataset original usa otra moneda.
