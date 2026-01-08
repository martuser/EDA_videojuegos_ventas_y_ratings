# ** 🎮 EDA – Venta de videojuegos y su rating (1976–2017) 🎮 **

## 1) Descripción breve del proyecto
Este proyecto realiza un **Análisis Exploratorio de Datos (EDA)** sobre un dataset de videojuegos con **ventas por región** y variables de **percepción** (puntuaciones y número de reseñas de crítica profesional y usuarios), además de **género, plataforma, publisher y rating ESRB**.

**Objetivo de negocio (enfoque cliente):**
- Identificar **qué factores se asocian con mayores ventas** (globales y regionales).
- Entender si pesa más la **crítica profesional** o la **valoración de usuarios**.
- Extraer **insights** para decisiones de **catálogo, plataforma, región y marketing** a la hora de dedicar recursos para crear un videojuego nuevo.

---

## 2) Hipótesis planteadas
### 2.1. ¿A qué hacen más caso los usuarios?
1. **Relación score–ventas:** ¿`Global_Sales` aumenta cuando aumentan `Critic_Score` y/o `User_Score`?  
   - ¿Cambia la relación por región (NA/EU/JP/Other)?
2. **¿Qué pesa más?:** ¿correlaciona mejor con ventas la crítica profesional o la de usuarios?
3. **Brecha crítico vs usuario:** ¿cómo varía la diferencia `Critic_Score` vs `User_Score` según:
   - género, plataforma y año?
4. **Efecto del volumen de reviews:** ¿más `Critic_Count` / `User_Count` implica más ventas?
   - ¿cómo varía por año, región, género y plataforma?
5. **Evolución temporal:** ¿cómo evolucionan scores, counts y la brecha a lo largo de los años?

### 2.2. ¿Qué se vende más?
6. **Top géneros y su evolución:** géneros con mayores ventas y cómo cambia el ranking por año/época.
7. **Top plataformas y ciclo de vida:** subida, pico y caída de ventas por plataforma con el tiempo.
8. **Publishers:** qué publishers concentran más ventas y cómo cambia su peso con el tiempo.
9. **Diferencias regionales:** comparar NA/EU/JP/Other:
   - qué géneros/plataformas funcionan mejor en cada región.
10. **ESRB y ventas:** si el rating afecta a ventas globales y por región, y si depende de otras variables.

---

## 3) Tecnologías utilizadas
- **Python** (EDA y visualización)
- Librerías: **pandas**, **numpy**, **matplotlib**, **seaborn** *(ajusta según lo que uséis realmente)*
- Entorno: **Jupyter Notebook / VSCode**
- Control de versiones: **Git + GitHub**

---

## 4) Estructura del repositorio
```text
├── src/                               # Código fuente y scripts auxiliares
│    ├── data/                         # Almacén de datos
│       ├── raw/                       # Datos originales (tal cual se descargaron)
│       └── processed/                 # Datos limpios y transformados listos para el análisis
│           └── video_game_sales_limpio.csv
│    ├── img/                          # Recursos visuales
│    ├── notebooks/                    # Jupyter Notebooks numerados por orden de ejecución
│        ├── 01_Limpieza_Datos.ipynb   # Preprocesamiento, gestión de nulos y tipos
│        └── 02_Analisis_EDA.ipynb     # Análisis exploratorio, visualización y test
│    ├── utils/                        # Funciones reutilizables para limpieza y ploteo
│    ├── requirements.txt              # Librerías necesarias para replicar el entorno
│
│
├── .gitignore                         # Archivos y carpetas a ignorar por git
├── Memoria.pdf                        # Documento detallado con hallazgos de negocio
├── Presentacion.pptx                  # Presentación usada para la exposición de los hallazgos
└── README.md                          # Este archivo
```
---

## 5) Instrucciones de reproducción
1. Clona el repositorio:
   - `git clone <URL_DEL_REPO>`
2. (Opcional) Crea y activa un entorno virtual y regístralo como kernel
3. Instala dependencias (si aplica):
   - `pip install -r requirements.txt`
4. Ejecuta el notebook:
   - Abrir `main.ipynb` y ejecutar todas las celdas en orden.

---

## 6) Principales conclusiones
## Principales conclusiones (borrador – para reescribir tras el EDA final)

### Conclusiones clave (versión corta – estilo ejecutivo)
- **La crítica profesional es un predictor más consistente de ventas** que la valoración de usuarios en el mercado global (especialmente en NA y EU), lo que sugiere que la visibilidad en medios especializados sigue influyendo en el rendimiento comercial.
- **Japón se comporta de forma distinta**: el peso relativo de la valoración de usuarios y la preferencia por ciertos géneros/plataformas difiere del patrón de NA/EU, por lo que conviene una estrategia de lanzamiento específica por región.
- **El volumen de reseñas (sobre todo de crítica) se asocia con mayores ventas**, actuando como proxy de notoriedad y cobertura mediática; el efecto de las reseñas de usuarios es más irregular.
- **Existe una brecha sistemática entre crítica y usuarios**: los usuarios tienden a puntuar ligeramente más alto en promedio, pero la brecha varía por género y plataforma, indicando posibles fenómenos de “expectativas” o “polarización”.
- **El mix de ventas está dominado por un número reducido de géneros y plataformas**, con ciclos de vida claros: crecimiento, pico y declive. Esto permite planificar ventanas óptimas de lanzamiento y soporte comercial.
- **El mercado muestra concentración moderada**: los títulos/publishers líderes se llevan una parte relevante de las ventas, pero existe “cola larga” donde muchos juegos aportan ventas menores.

---

### Hallazgos detallados (versión ampliada – por hipótesis)

#### A) ¿A qué hacen más caso los usuarios?
- **Relación score–ventas:** se observa una relación positiva entre puntuaciones y ventas, pero **moderada**; las puntuaciones ayudan a explicar ventas, aunque no son el único factor (género, plataforma, región y año también influyen).
- **Qué pesa más (crítica vs usuarios):** la **crítica profesional** correlaciona mejor con ventas globales que la puntuación de usuarios, especialmente en **NA y EU**. En **JP**, la señal de usuarios gana relevancia relativa.
- **Brecha crítico vs usuario:** la diferencia entre crítica y usuarios **no es constante**:
  - En géneros de consumo masivo (p.ej. *Sports/Action*) la crítica puede ser más exigente o, en ocasiones, más favorable que los usuarios según plataforma y año.
  - En géneros de nicho (p.ej. *Role-Playing*) los usuarios suelen puntuar más alto, probablemente por efecto “fan base”.
- **Counts y ventas:** un mayor número de reseñas (especialmente `Critic_Count`) se asocia con más ventas, indicando que **cobertura/visibilidad** acompaña al éxito comercial. `User_Count` también tiende a subir con ventas, pero con más ruido (efecto de comunidad, polémicas, etc.).
- **Evolución temporal:** con el tiempo aumentan los volúmenes de reseñas (más participación y plataformas online) y la brecha crítica–usuario se vuelve más variable, especialmente a partir de la expansión del review bombing / campañas de opinión en ciertos periodos.

#### B) ¿Qué se vende más?
- **Top géneros:** las ventas globales se concentran en unos pocos géneros (p.ej. *Action* y *Sports*), aunque el ranking cambia por épocas (auge de ciertos géneros en generaciones de consola concretas).
- **Top plataformas y ciclo de vida:** las plataformas líderes muestran un patrón típico:
  1) lanzamiento y adopción inicial  
  2) fase de crecimiento (catálogo + base instalada)  
  3) pico (mejor rendimiento)  
  4) declive (siguiente generación)
- **Publishers:** un conjunto reducido de publishers acumula gran parte de las ventas globales; sin embargo, su peso cambia con el tiempo (entrada/salida de actores y cambios de estrategia).
- **Diferencias regionales:** cada región tiene “drivers” distintos:
  - NA/EU tienden a favorecer géneros mainstream y plataformas con gran base instalada.
  - JP muestra mayor peso de géneros concretos (p.ej. *Role-Playing*) y preferencias de plataforma diferenciadas.
- **ESRB y ventas:** el rating se asocia con el potencial de ventas:
  - ratings más “familiares” (p.ej. **E / E10+**) tienden a tener mejor rendimiento en NA/EU por mercado más amplio,
  - mientras que ratings más restrictivos muestran ventas más concentradas en ciertos géneros y plataformas.
- **Concentración del mercado:** el top N (juegos/publishers) captura una parte relevante del total, pero no absoluta; existe una “cola larga” que sugiere oportunidades para títulos de nicho con estrategia regional adecuada.

---

### Implicaciones (para cliente)
- **NA/EU:** priorizar estrategia de **PR y crítica** (medios especializados, previews, notas de prensa, acuerdos de visibilidad), además de optimizar el lanzamiento por plataformas con mayor tracción.
- **JP:** reforzar estrategia de **comunidad** (activaciones, influencers locales, engagement post-lanzamiento) y ajustar el mix de género/plataforma.
- **Go-to-market:** segmentar campañas por **región + plataforma + género**, y usar el volumen de reseñas como indicador temprano de tracción (early signal).

---

## 7) Autores
- Maitane Barreira Castelao – GitHub: [[link](https://github.com/maitanebarreira-commits)]
- Pablo Vázquez Argüelles – GitHub: [[link](https://github.com/pablovazqueez)] 
- Marta Estévez Rodríguez – GitHub: [[link](https://github.com/martuser)]
