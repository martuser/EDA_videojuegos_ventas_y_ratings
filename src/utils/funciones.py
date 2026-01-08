import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
RUTA_GRAFICOS = "./src/img"

def guardar_figura(nombre_archivo, ruta):

    if ruta:
        os.makedirs(ruta, exist_ok=True)
        
        # Limpiamos el nombre del archivo de caracteres extraños si fuera necesario
        nombre_limpio = nombre_archivo.replace(" ", "_").replace(":", "").replace("/", "-")
        path_completo = os.path.join(ruta, f"{nombre_limpio}.jpg")
        
        # Guardamos
        plt.savefig(path_completo, bbox_inches='tight', dpi=150)
        print(f"Gráfico guardado: {path_completo}")


def limpiar_df(df):
    columnas_con_nulos_permitidos = [
        "Critic_Score",
        "Critic_Count",
        "User_Score",
        "User_Count",
        "Rating"
    ]

    # Filtrar y forzar copia para evitar SettingWithCopyWarning
    df = df.dropna(
        subset=[col for col in df.columns if col not in columnas_con_nulos_permitidos]
    ).copy()

    df.loc[:, "Critica_Profesional"] = np.where(
        df["Critic_Score"].notnull() & df["Critic_Count"].notnull(),
        "Sí",
        "No"
    )

    df.loc[:, "Critica_Usuario"] = np.where(
        df["User_Score"].notnull() & df["User_Count"].notnull(),
        "Sí",
        "No"
    )

    df.loc[:, "Tiene_Rating"] = np.where(
        df["Rating"].notnull(),
        "Sí",
        "No"
    )

    return df

def resumen_scores(df, engagement_min=50):

    df_scores = df.dropna(subset=["Global_Sales"]).copy()

    df_both_scores = df.dropna(subset=["Critic_Score", "User_Score"]).copy()

    df_high_engagement = df[df["User_Count"].fillna(0) >= engagement_min].copy()

    print("Total:", df.shape[0])
    print(
        "Con al menos algún score:",
        df.dropna(subset=["Critic_Score", "User_Score"], how="all").shape[0]
    )
    print("Con ambos scores:", df_both_scores.shape[0])
    print(f"High engagement (User_Count>={engagement_min}):", df_high_engagement.shape[0])

    return {
        "df_scores": df_scores,
        "df_both_scores": df_both_scores,
        "df_high_engagement": df_high_engagement
    }

def panorama_mercado(df):
    df0 = df.copy()

    # Ventas con log (mejor para scatter)
    df0["Global_Sales_log1p"] = np.log1p(df0["Global_Sales"])

    # Distribución de ventas globales
    plt.figure(figsize=(8, 5))
    plt.hist(df0["Global_Sales"].dropna(), bins=40)
    plt.title("Distribución de Global_Sales (millones)")
    plt.xlabel("Global_Sales")
    plt.ylabel("Nº juegos")
    plt.tight_layout()
    # Guardar antes de mostrar
    guardar_figura("distribucion_ventas_globales", RUTA_GRAFICOS)
    plt.show()


    plt.figure(figsize=(8, 5))
    plt.hist(df0["Global_Sales_log1p"].dropna(), bins=40)
    plt.title("Distribución de Global_Sales (log1p)")
    plt.xlabel("log1p(Global_Sales)")
    plt.ylabel("Nº juegos")
    plt.tight_layout()
    guardar_figura("distribucion_ventas_log", RUTA_GRAFICOS)
    plt.show()

    # Peso regional (share)
    region_totals = (
        df0[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]]
        .sum()
        .sort_values(ascending=False)
    )

    region_share = (region_totals / region_totals.sum() * 100).round(1)

    plt.figure(figsize=(7, 4))
    region_share.sort_values().plot(kind="barh")
    plt.title("Ventas por región (%)")
    plt.xlabel("% del total")
    plt.tight_layout()
    guardar_figura("ventas_por_region", RUTA_GRAFICOS)
    plt.show()

    return df0, region_share

def analizar_correlacion(df, column_score):


    # 1. Copia del DataFrame
    df_copia = df.copy()

    # 2. Cálculo de la correlación
    correlacion = df_copia["Global_Sales"].corr(df_copia[column_score])

    # 3. Interpretación de la correlación
    abs_corr = abs(correlacion)

    if abs_corr < 0.2:
        interpretacion = "muy débil o inexistente"
    elif abs_corr < 0.4:
        interpretacion = "débil"
    elif abs_corr < 0.6:
        interpretacion = "moderada"
    elif abs_corr < 0.8:
        interpretacion = "fuerte"
    else:
        interpretacion = "muy fuerte"

    # 4. Mostrar resultados
    print(f"La correlación entre la crítica y las ventas globales es: {correlacion:.2f}")
    print(f"Interpretación: correlación {interpretacion}")

    # 5. Visualización
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=df_copia,
        x=column_score,
        y="Global_Sales",
        alpha=0.5
    )
    plt.title("Relación entre puntuación de la crítica y ventas globales")
    plt.xlabel("Puntuación de la crítica")
    plt.ylabel("Ventas globales (millones)")
    plt.grid(True)
    guardar_figura(f"correlacion_{column_score}", RUTA_GRAFICOS)
    plt.show()
    return correlacion

def comparar_correlaciones(correlacion_profesionales, correlacion_usuarios):
    plt.figure(figsize=(10, 6))
    labels = ["Crítica Profesional", "Crítica Usuarios"]
    valores = [correlacion_profesionales, correlacion_usuarios]
    plt.bar(labels, valores, color= ["blue", "green"])
    plt.ylabel("Coeficiente de Correlación")
    plt.title("Comparativa de Influencia en Ventas Globales")
    plt.ylim(0, 1) # El límite sería 1, que es una correlación directa
    guardar_figura("comparativa_correlaciones_barras", RUTA_GRAFICOS)
    plt.show()

def analizar_brecha_scores(df_input, titulo="General", color_grafico='purple'):

    data = df_input.copy()
    # Asumimos que Critic es base 100 y User base 10
    data["Score_dif"] = data["Critic_Score"] - (data["User_Score"] * 10)
  
    if "Global_Sales" in data.columns and "Critic_Score" in data.columns:
        corr = data["Global_Sales"].corr(data["Critic_Score"])
        print(f"Correlación Ventas Globales vs Critic Score: {corr:.4f}")
    
    print(f"Estadísticas de la Brecha (Score_dif):")
    print(data["Score_dif"].describe())

    plt.figure(figsize=(10, 6))
    sns.histplot(data['Score_dif'], kde=True, color=color_grafico)
    plt.title(f'Distribución de la Brecha (Crítica - Usuario) - {titulo}')
    plt.axvline(0, color='red', linestyle='--', label='Coincidencia (0)')
    plt.xlabel('Diferencia de Puntos (Critic - User*10)')
    plt.legend()
    guardar_figura(f"brecha_scores_{titulo}", RUTA_GRAFICOS)
    plt.show()

def auditar_anio(df_input, anio):
    subset = df_input[df_input["Year_of_Release"] == anio]
    print(f"\n--- Auditoría del año {anio} ---")
    print(f"Total juegos encontrados: {len(subset)}")
  
    cols = ["Name", "User_Score", "Critic_Score", "User_Count"]
    cols_existentes = [c for c in cols if c in df_input.columns]
    
    print(subset[cols_existentes].head(10)) 
    return subset


def visualizar_evolucion_temporal(df_input, start_year=None, titulo="Evolución Temporal"):
    data = df_input.copy()
    
    if start_year:
        data = data[data["Year_of_Release"] >= start_year]
        titulo = f"{titulo} (Desde {start_year})"

    if "Score_dif" not in data.columns:
        data["Score_dif"] = data["Critic_Score"] - (data["User_Score"] * 10)

    cols_interes = ["Critic_Score", "User_Score", "Score_dif"]
    tendencias = data.groupby("Year_of_Release")[cols_interes].mean()
  
    tendencias["User_Score_100"] = tendencias["User_Score"] * 10
    plt.figure(figsize=(12, 6))

  
    plt.plot(tendencias.index, tendencias["Critic_Score"], label="Nota Críticos", 
             color="blue", marker="o", linewidth=2, alpha=0.8)
    plt.plot(tendencias.index, tendencias["User_Score_100"], label="Nota Usuarios (x10)", 
             color="green", marker="s", linewidth=2, alpha=0.8)
    plt.plot(tendencias.index, tendencias["Score_dif"], label="Brecha (Diferencia)", 
             color="red", linestyle="--", linewidth=2)

    plt.axhline(0, color="black", linewidth=1, alpha=0.5, label='Consenso (0)')
    plt.title(titulo, fontsize=14)
    plt.xlabel("Año de Lanzamiento", fontsize=12)
    plt.ylabel("Puntuación / Diferencia", fontsize=12)
    plt.legend()
    plt.grid(True, linestyle=":", alpha=0.6)
    guardar_figura(f"evolucion_temporal_{start_year if start_year else 'full'}", RUTA_GRAFICOS)
    plt.show()

def definir_epoca(year):
    """Clasifica el año en una época predefinida."""
    if year <= 2000:
        return "1. Retro (Hasta 2000)"
    elif year <= 2010:
        return "2. Consolas Oro (2001-2010)"
    else:
        return "3. Moderna (2011+)"

def analizar_rendimiento_generos(df_input):
    df = df_input.copy()
    
    # 1. Ventas Totales (Volumen)
    ventas_genero = df.groupby("Genre")["Global_Sales"].sum().sort_values(ascending=False)
    
    plt.figure(figsize=(12, 6))
    # NOTA: En versiones nuevas de Seaborn, si usas palette sin hue, da warning. 
    # Asignamos hue=y y legend=False para evitarlo.
    sns.barplot(
        x=ventas_genero.values, 
        y=ventas_genero.index, 
        hue=ventas_genero.index, 
        palette="rocket", 
        legend=False
    )
    plt.title("Ventas Globales Totales por Género")
    plt.xlabel("Millones de Unidades Vendidas")
    plt.ylabel("Género")
    guardar_figura("ventas_totales_genero", RUTA_GRAFICOS)
    plt.show()

    # Calculamos la media
    eficiencia_genero = df.groupby("Genre")["Global_Sales"].mean()
    
    plt.figure(figsize=(12, 6))
    # Usamos el 'order' de ventas_genero para mantener el mismo orden que el gráfico anterior
    # Esto facilita comparar visualmente "Cantidad vs Calidad"
    sns.barplot(
        x=eficiencia_genero.values, 
        y=eficiencia_genero.index, 
        order=ventas_genero.index,  # Clave: Mismo orden que el gráfico 1
        hue=ventas_genero.index,
        palette="mako",
        legend=False
    )
    plt.title("Ventas Promedio por Título (Eficiencia)")
    plt.xlabel("Ventas Medias (Millones por juego)")
    plt.ylabel("Género")
    guardar_figura("ventas_promedio_eficiencia_genero", RUTA_GRAFICOS)
    plt.show()

def analizar_evolucion_cuota_mercado(df_input):

    df = df_input.copy()
    
    # Creamos la columna época usando la función auxiliar
    df["Epoca"] = df["Year_of_Release"].apply(definir_epoca)
    
    # Pivotamos para conseguir la estructura necesaria para el stacked plot
    # Rellenamos con 0 por si en alguna época no hubo lanzamientos de un género
    epoca_genero = df.groupby(["Epoca", "Genre"])["Global_Sales"].sum().unstack().fillna(0)
    
    # Calculamos porcentajes (dividiendo cada fila por su suma)
    epoca_perc = epoca_genero.div(epoca_genero.sum(axis=1), axis=0) * 100
    
    # Visualización
    # Usamos pandas plot directo ya que maneja muy bien los stacked bars
    ax = epoca_perc.plot(kind="bar", stacked=True, figsize=(14, 7), colormap="tab20")
    
    plt.title("Cuota de Mercado por Género según la Época (%)")
    plt.ylabel("Porcentaje de Ventas Totales")
    plt.xlabel("Época")
    
    # Ajustamos la leyenda para que no tape el gráfico
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title="Género")
    plt.tight_layout() # Ajusta los márgenes para que entre la leyenda
    guardar_figura("evolucion_cuota_mercado_generos", RUTA_GRAFICOS)
    plt.show()

def analizar_ciclo_vida_plataformas(df_input, n_top=5):
    df = df_input.copy()
    
    # 1. Identificar las Top N plataformas
    top_plat = df.groupby("Platform")["Global_Sales"].sum().nlargest(n_top).index.tolist()
    
    print(f"Top {n_top} Plataformas analizadas: {top_plat}")
    
    # 2. Filtrar el dataframe para quedarnos solo con esas plataformas
    df_filtrado = df[df["Platform"].isin(top_plat)].copy()
    
    if df_filtrado["Platform"].dtype.name == 'category':
        df_filtrado["Platform"] = df_filtrado["Platform"].cat.remove_unused_categories()

    # 4. Agrupación para el gráfico
    evolucion_plat = df_filtrado.groupby(["Year_of_Release", "Platform"])["Global_Sales"].sum().reset_index()

    plt.figure(figsize=(14, 7))
    sns.lineplot(
        data=evolucion_plat, 
        x="Year_of_Release", 
        y="Global_Sales", 
        hue="Platform", 
        hue_order=top_plat,  # Mantiene el orden del ranking
        marker="o", 
        linewidth=2.5
    )

    plt.title(f"Ciclo de Vida de las Top {n_top} Plataformas (Ventas por Año)", fontsize=15)
    plt.xlabel("Año de Lanzamiento")
    plt.ylabel("Ventas Globales (Millones)")
    plt.grid(True, alpha=0.3)
    
    # Leyenda fuera del gráfico para no tapar datos
    plt.legend(title="Consola", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    guardar_figura(f"ciclo_vida_top_{n_top}_plataformas", RUTA_GRAFICOS)
    plt.show()

def analizar_top_publishers(df_input, n_top=10, start_year=None, end_year=None):
    df_filtrado = df_input.copy()
    
    # Variable para el título del gráfico
    periodo_texto = "Histórico Completo"

    # 2. Aplicamos filtros de fecha si existen
    if start_year is not None:
        df_filtrado = df_filtrado[df_filtrado["Year_of_Release"] >= start_year]
        periodo_texto = f"Desde {start_year}"
        
    if end_year is not None:
        df_filtrado = df_filtrado[df_filtrado["Year_of_Release"] <= end_year]
        # Ajustamos el texto del título
        if start_year is not None:
            periodo_texto = f"({start_year} - {end_year})"
        else:
            periodo_texto = f"Hasta {end_year}"

    # 3. Agrupamos y sacamos el Top N (sobre los datos ya filtrados)
    top_publishers = df_filtrado.groupby("Publisher")["Global_Sales"].sum().nlargest(n_top)

    # 4. Visualización
    plt.figure(figsize=(12, 6))
    
    sns.barplot(
        x=top_publishers.values, 
        y=top_publishers.index, 
        hue=top_publishers.index, 
        palette="coolwarm", 
        legend=False
    )

    plt.title(f"Top {n_top} Publishers por Ventas - {periodo_texto}")
    plt.xlabel("Millones de copias vendidas")
    plt.ylabel("Publisher")
    
    # Limpiamos el texto del periodo para que sea un nombre de archivo válido
    sufijo = periodo_texto.replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_to_")
    guardar_figura(f"top_{n_top}_publishers_{sufijo}", RUTA_GRAFICOS)
    plt.show()

def visualizar_lideres_regionales(df_input, start_year=None, end_year=None):

    df = df_input.copy()
    
    # 1. Filtro de fechas
    periodo_texto = "Histórico"
    if start_year:
        df = df[df["Year_of_Release"] >= start_year]
        periodo_texto = f"Desde {start_year}"
    if end_year:
        df = df[df["Year_of_Release"] <= end_year]
        periodo_texto += f" hasta {end_year}"

    # Diccionario para mapear nombres de columnas a nombres bonitos
    regiones_map = {
        "NA_Sales": "Norteamérica",
        "EU_Sales": "Europa",
        "JP_Sales": "Japón"
    }
    col_regiones = ["NA_Sales", "EU_Sales", "JP_Sales"]
    
    # 2. Configuración del Grid de Gráficos (2 filas, 3 columnas)
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(18, 10))
    fig.suptitle(f"Líderes Regionales: Géneros y Plataformas ({periodo_texto})", fontsize=16, y=1.02)

    # 3. Iteramos por cada región (cada columna del gráfico)
    for i, region in enumerate(col_regiones):
        nombre_region = regiones_map[region]
        
        # --- FILA 1: GÉNEROS ---
        top_gen = df.groupby("Genre")[region].sum().nlargest(5)
        
        sns.barplot(
            x=top_gen.index, 
            y=top_gen.values, 
            ax=axes[0, i], 
            hue=top_gen.index, 
            palette="Blues_r", # Azul degradado
            legend=False
        )
        axes[0, i].set_title(f"Top Géneros - {nombre_region}")
        axes[0, i].set_ylabel("Ventas (Millones)")
        axes[0, i].set_xlabel("")
        axes[0, i].tick_params(axis='x', rotation=45)

        # Imprimimos el dato por consola también (como tu código original)
        if not top_gen.empty:
            print(f"[{nombre_region}] Género líder: {top_gen.index[0]} ({top_gen.values[0]:.1f}M)")

        # --- FILA 2: PLATAFORMAS ---
        top_plat = df.groupby("Platform")[region].sum().nlargest(5)
        
        sns.barplot(
            x=top_plat.index, 
            y=top_plat.values, 
            ax=axes[1, i], 
            hue=top_plat.index,
            palette="Reds_r", # Rojo degradado
            legend=False
        )
        axes[1, i].set_title(f"Top Plataformas - {nombre_region}")
        axes[1, i].set_ylabel("Ventas (Millones)")
        axes[1, i].set_xlabel("")
        
        if not top_plat.empty:
            print(f"[{nombre_region}] Plataforma líder: {top_plat.index[0]} ({top_plat.values[0]:.1f}M)")

    # Ajuste final para que no se solapen los textos
    plt.tight_layout()
    sufijo = periodo_texto.replace(" ", "_").replace(":", "")
    guardar_figura(f"lideres_regionales_{sufijo}", RUTA_GRAFICOS)
    
    plt.show()

def analizar_ventas_por_rating(df_input, start_year=None, end_year=None):

    df = df_input.copy()
    
    # 1. Filtro de fechas y texto para el título
    periodo_texto = "Histórico"
    if start_year:
        df = df[df["Year_of_Release"] >= start_year]
        periodo_texto = f"Desde {start_year}"
    if end_year:
        df = df[df["Year_of_Release"] <= end_year]
        periodo_texto += f" hasta {end_year}"

    # 2. Cálculo de la media
    # Agrupamos y ordenamos de mayor a menor venta promedio
    ventas_esrb_media = df.groupby("Rating")["Global_Sales"].mean().sort_values(ascending=False)

    # 3. Contexto (Conteo)
    # Es importante saber si la media alta es por 1 solo juego o por 1000
    conteo_esrb = df.groupby("Rating")["Global_Sales"].count()
    
    print(f"\n--- Contexto: Cantidad de juegos por Rating ({periodo_texto}) ---")
    # Mostramos el conteo reordenado según el ranking de ventas para comparar fácil
    print(conteo_esrb.reindex(ventas_esrb_media.index))

    # 4. Visualización
    plt.figure(figsize=(10, 6))
    
    # SOLUCIÓN DEPRECACIÓN:
    # Usamos hue=index y legend=False. Esto evita el aviso de futuras versiones de Seaborn.
    sns.barplot(
        x=ventas_esrb_media.index, 
        y=ventas_esrb_media.values, 
        hue=ventas_esrb_media.index, 
        palette="Blues_r", 
        legend=False
    )

    plt.title(f"Ventas Promedio por Juego según Rating ESRB - {periodo_texto}")
    plt.ylabel("Millones de copias (Media por título)")
    plt.xlabel("Clasificación de Edad")
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    sufijo = periodo_texto.replace(" ", "_").replace(":", "")
    guardar_figura(f"ventas_media_rating_esrb_{sufijo}", RUTA_GRAFICOS)
        
    plt.show()

def analizar_composicion_esrb_genero(df_input, start_year=None, end_year=None, ruta_guardado=None):
    """
    Genera un gráfico de barras apiladas que muestra qué géneros componen
    cada categoría de edad (ESRB).
    """
    df = df_input.copy()
    
    # 1. Filtro de fechas
    periodo_texto = "Histórico"
    if start_year:
        df = df[df["Year_of_Release"] >= start_year]
        periodo_texto = f"Desde {start_year}"
    if end_year:
        df = df[df["Year_of_Release"] <= end_year]
        periodo_texto += f" hasta {end_year}"

    # 2. Creación de la Tabla Cruzada (Pivot Table)
    # Usamos 'Name' para contar cuántos juegos hay. fillna(0) es vital para visualización limpia.
    esrb_genero_count = df.pivot_table(
        index="Rating", 
        columns="Genre", 
        values="Name", 
        aggfunc="count"
    ).fillna(0)

    # 3. Visualización
    # Usamos pandas plot directo, es el estándar para 'stacked bars'
    ax = esrb_genero_count.plot(
        kind="bar", 
        stacked=True, 
        figsize=(12, 7), 
        colormap="tab20",
        width=0.8 # Hacemos las barras un poco más anchas
    )

    plt.title(f"Distribución de Géneros dentro de cada Rating ESRB - {periodo_texto}")
    plt.ylabel("Cantidad de Juegos Lanzados")
    plt.xlabel("Clasificación ESRB")
    
    # Rotamos etiquetas del eje X para que se lean bien (0 grados = horizontal)
    plt.xticks(rotation=0) 

    # Leyenda fuera para no tapar datos
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", title="Géneros")
    plt.tight_layout()

    # 4. Guardado
    sufijo = periodo_texto.replace(" ", "_").replace(":", "")
    guardar_figura(f"composicion_esrb_generos_{sufijo}", RUTA_GRAFICOS)

    plt.show()
