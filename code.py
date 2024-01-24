# %% [markdown]
# # ¡Llena ese carrito!

# %% [markdown]
# # Introducción
# 
# Instacart es una plataforma de entregas de comestibles donde la clientela puede registrar un pedido y hacer que se lo entreguen, similar a Uber Eats y Door Dash.

# %% [markdown]
# ## Diccionario de datos
# 
# Hay cinco tablas en el conjunto de datos, todas para hacer el preprocesamiento de datos y el análisis exploratorio de datos. A continuación se muestra un diccionario de datos que enumera las columnas de cada tabla y describe los datos que contienen.
# 
# - `instacart_orders.csv`: cada fila corresponde a un pedido en la aplicación Instacart.
#     - `'order_id'`: número de ID que identifica de manera única cada pedido.
#     - `'user_id'`: número de ID que identifica de manera única la cuenta de cada cliente.
#     - `'order_number'`: el número de veces que este cliente ha hecho un pedido.
#     - `'order_dow'`: día de la semana en que se hizo el pedido (0 si es domingo).
#     - `'order_hour_of_day'`: hora del día en que se hizo el pedido.
#     - `'days_since_prior_order'`: número de días transcurridos desde que este cliente hizo su pedido anterior.
# - `products.csv`: cada fila corresponde a un producto único que pueden comprar los clientes.
#     - `'product_id'`: número ID que identifica de manera única cada producto.
#     - `'product_name'`: nombre del producto.
#     - `'aisle_id'`: número ID que identifica de manera única cada categoría de pasillo de víveres.
#     - `'department_id'`: número ID que identifica de manera única cada departamento de víveres.
# - `order_products.csv`: cada fila corresponde a un artículo pedido en un pedido.
#     - `'order_id'`: número de ID que identifica de manera única cada pedido.
#     - `'product_id'`: número ID que identifica de manera única cada producto.
#     - `'add_to_cart_order'`: el orden secuencial en el que se añadió cada artículo en el carrito.
#     - `'reordered'`: 0 si el cliente nunca ha pedido este producto antes, 1 si lo ha pedido.
# - `aisles.csv`
#     - `'aisle_id'`: número ID que identifica de manera única cada categoría de pasillo de víveres.
#     - `'aisle'`: nombre del pasillo.
# - `departments.csv`
#     - `'department_id'`: número ID que identifica de manera única cada departamento de víveres.
#     - `'department'`: nombre del departamento.

# %% [markdown]
# # Paso 1. Descripción de los datos
# 
# Lee los archivos de datos (`/datasets/instacart_orders.csv`, `/datasets/products.csv`, `/datasets/aisles.csv`, `/datasets/departments.csv` y `/datasets/order_products.csv`) con `pd.read_csv()` usando los parámetros adecuados para leer los datos correctamente. Verifica la información para cada DataFrame creado.
# 

# %%
# importar librerías
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# %% [markdown]
# ## Plan de solución
# 
# Paso 1. Descripción de los datos.   
#   Para describir y entender los datos, primero leeremos los dataframes con el metodo csv, para ver su separador, si es diferente a **','** lo cambiaremos por el correcto con el parametro 'sep', posteriormente aplicaremos el método info() y describe() para todos los dataframes, con el fin de ver que tipo de datos tenemos, cuantas columnas y filas.   
#   
#   Además se revisarán las primeras filas de cada dataframe, para entender un poco los datos. 

# %%
# leer conjuntos de datos en los DataFrames
df_instacart=pd.read_csv('instacart_orders.csv',sep=';')
df_products=pd.read_csv('products.csv',sep=';')
df_aisles=pd.read_csv('aisles.csv',sep=';')
df_departments=pd.read_csv('departments.csv',sep=';')
df_order_products=pd.read_csv('order_products.csv',sep=';')

# %%
# mostrar información del DataFrame
print(df_instacart.head(5))
#Llamamos la función info:
df_instacart.info()
#Llamamos la función describe:
df_instacart.describe()

# %%
# mostrar información del DataFrame
print(df_products.head(5))
#Llamamos la función info:
df_products.info()
#Llamamos la función describe:
df_products.describe()

# %%
# mostrar información del DataFrame
print(df_aisles.head(10))
#Llamamos la función info:
df_aisles.info()
#Llamamos la función describe:
df_aisles.describe()

# %%
# mostrar información del DataFrame
print(df_departments.head(10))
#Llamamos la función info:
df_departments.info()
#Llamamos la función describe:
df_departments.describe()

# %%
# mostrar información del DataFrame
print(df_order_products.head(5))
#Llamamos la función info:
df_order_products.info()
#Llamamos la función describe:
df_order_products.describe()

# %% [markdown]
# ## Conclusiones
# 
# Paso 1. Descripción de los datos:
# 1. El dataframe instacart tiene información detallada de la actividad de los clientes respecto a las ordenes, el numero de veces y el tiempo en que se hizo una orden. Tiene 478967 filas y 6 columnas y se puede ver que tiene valores nulos en su última columna, los analizaremos más adelante.
# 
# 2. El dataframe products tiene información de cada producto, junto con su id y los id's que relacionan cada producto con su departamento y categoría de pasillo. Tiene 49694 filas y 4 columnas, con valores nulos en el nombre del producto.
# 
# 3. El dataframe aisles representa cada categoría de pasillo junto con su id. Tiene 134 filas y 2 columnas, no tiene valores nulos.
# 
# 4. El dataframe department, representa cada departamento con su id. Tiene 21 filas y 2 columnas, no tiene nulos.
# 
# 5. El dataframe order_products contiene la relación del id del producto con el id de la orden, también da información acerca del historico de las compras y si secuencia de compra en el carrito. Tiene 4343007 filas y 4 columnas.

# %% [markdown]
# # Paso 2. Preprocesamiento de los datos

# %% [markdown]
# ## Plan de solución
# 
# Paso 2. Preprocesamiento de los datos:  
#   - Primero vamos a identificar la cantidad de valores ausentes por columna, usando isna().sum(), para ver que tan significativo es el impacto de los ausentes, y verificamos que tan importante es la ausencia de los valores en cada categoría teniendo en cuenta la lógica del dataframe.
# 
# - Segundo, vamos a verificar si nuestros ausentes son de variables categóricas o cuantitativas. Si son categóricas verificamos si tiene un patrón para asignar estos ausentes, si son totalmente aleatorios los ausentes, debemos asignar una palabra para identificarlos. En caso de ser cuantitativos verificamos si hay atipicos, si tiene atipicos podemos rellenar con fillna() los ausentes usando la mediana, si no hay atipicos, podemos usar la media.
# 
# - Tercero, con respecto a los duplicados vamos a utilizar el método duplicated() o value_counts() para identificarlos, y verificar si son importantes o si simplemente los podemos borrar con drop_duplicates(), despues verificamos a mano si hay duplicados por distinción de minusculas o mayusculas, con el fin de limpiar nuestros datos.

# %% [markdown]
# ## Encuentra y elimina los valores duplicados.

# %% [markdown]
# ### `orders` data frame

# %%
# Revisa si hay pedidos duplicados
print('Numero de ordenes duplicadas: ',df_instacart['order_id'].duplicated().sum())
print()
print(df_instacart['order_id'].value_counts().head(15))
print()


# %%
#Realizamos un filtro con el método query() para revisar si los duplicados tienen toda la línea duplicada 
lista=df_instacart['order_id'][df_instacart['order_id'].duplicated()==True]
print(df_instacart.query('order_id in @lista').sort_values(by='order_id'))

# %% [markdown]
# Tenemos ordenes duplicadas que debemos eliminar, la particularidad que tienen es que todos son el miercoles a las 2 de la mañama.

# %%
# Basándote en tus hallazgos,
# Verifica todos los pedidos que se hicieron el miércoles a las 2:00 a.m.
print('Número de pedidos que se hicieron el miércoles a las 2:00 a.m: ',df_instacart[(df_instacart['order_dow']==3)&(df_instacart['order_hour_of_day']==2)]['order_id'].count())
print('Número de pedidos DUPLICADOS que se hicieron el miércoles a las 2:00 a.m: ',df_instacart[(df_instacart['order_dow']==3)&(df_instacart['order_hour_of_day']==2)]['order_id'].duplicated().sum())

# %% [markdown]
# ¿Qué sugiere este resultado?   
#     **Tenemos 15 valores duplicados en de compras a las 2 am, por lo tanto es necesario eliminarlos. Además las ordenes no se         deberían duplicar por que son únicas.**

# %%
# Elimina los pedidos duplicados
df_instacart=df_instacart.drop_duplicates(subset='order_id').reset_index(drop=True)

# %%
# Vuelve a verificar si hay filas duplicadas
print('Numero de ordenes duplicadas: ',df_instacart['order_id'].duplicated().sum())
print()
print(df_instacart['order_id'].value_counts().head(15))
print()

# %%
# Vuelve a verificar únicamente si hay IDs duplicados de pedidos
print('Número de duplicados: ',df_instacart['order_id'].duplicated().sum())

# %% [markdown]
#   **Eliminamos la líneas duplicadas y quedamos únicamente con una línea para cada orden como debe ser.**

# %% [markdown]
# ### `products` data frame

# %%
# Verifica si hay filas totalmente duplicadas
print('Número de duplicados: ',df_products.duplicated().sum())

# %%
# Verifica únicamente si hay IDs duplicadas de productos
print('Número de duplicados: ',df_products['product_id'].duplicated().sum())

# %%
# Revisa únicamente si hay nombres duplicados de productos (convierte los nombres a letras mayúsculas para compararlos mejor)
#Usamos el método upper() para convertir todos los nombres en minuscula
df_products['product_name']=df_products['product_name'].str.upper()
print(df_products['product_name'].value_counts().head(20))
print()
print('Valores únicos: ',df_products['product_name'].nunique(), 'Total nombres: ',df_products['product_name'].count())
print('Número de duplicados: ',df_products['product_name'].duplicated().sum())

# %%
# Revisa si hay nombres duplicados de productos no faltantes
#Usamos el parámetro dropna=True para descartar los ausentes
df_product_dupl=df_products['product_name'].value_counts(dropna=True)
print(df_product_dupl.head(20))

# %%
#Con esta línea verificamos si algunos de los nombres tienen líneas completamente duplicadas o si difieren en algunas columnas.

lista_2=df_products['product_name'][df_products['product_name'].duplicated()==True]
print(df_products.query('product_name in @lista_2').sort_values(by='product_name').head(20))


# %%
#filtro que contemple dos elementos: duplicados en product_name y que al mismo tiempo no sea un dato faltante.
filter_1=df_products['product_name'][(df_products['product_name'].duplicated()==True)&(~df_products['product_name'].isna())]
print(df_products.query('product_name in @filter_1').sort_values(by='product_name').head(20))

# %% [markdown]
#   Podemos ver que tenemos una gran cantidad de duplicados al cambiar todo a mayusculas, sin embargo, no los eliminaremos debido a que si eliminamos todas las filas de estos duplicados, perderiamos parte de los id que identifican a estos duplicados y que se asocian con los otros dataframes, podemos ver que parte de los duplicados son nulos, más especificamente 104 valores.

# %% [markdown]
# ### `departments` data frame

# %%
# Revisa si hay filas totalmente duplicadas
print('Número de duplicados: ',df_departments.duplicated().sum())

# %%
# Revisa únicamente si hay IDs duplicadas de productos
print('Número de duplicados: ',df_departments['department_id'].duplicated().sum())

# %% [markdown]
#   Podemos ver que no hay id's duplicados ni filas totalmente duplicadas, por lo cual no hay necesidad de eliminar nada.
# 

# %% [markdown]
# ### `aisles` data frame

# %%
# Revisa si hay filas totalmente duplicadas
print('Número de duplicados: ',df_aisles.duplicated().sum())

# %%
# Revisa únicamente si hay IDs duplicadas de productos
print('Número de duplicados: ',df_aisles['aisle_id'].duplicated().sum())

# %% [markdown]
#   Nuevamente vemos que no hay duplicados para el dataframe aisles, por lo tanto no hay necesidad de eliminar nada.

# %% [markdown]
# ### `order_products` data frame

# %%
# Revisa si hay filas totalmente duplicadas
print('Número de duplicados: ',df_order_products.duplicated().sum())

# %%
# Vuelve a verificar si hay cualquier otro duplicado engañoso
columns=['order_id','product_id']
#Utilizamos un for para revisar el numero de duplicados por columna
for column in columns:
    print(f'Número de duplicados de la columna {column}: ',df_order_products[column].duplicated().sum())
df_order_products['order_id'].value_counts(dropna=True)

# %% [markdown]
# 
#   Podemos ver que se ven duplicados en order_id y en product_id, sin embargo, esto se debe a que hay ordenes que tienen varios productos, por esto se repiten los numeros de orden, de la misma manera pasa con los productos, hay diferentes ordenes que tienen el mismo producto, por esta razón se pueden repetir los numeros de los productos.

# %% [markdown]
# Elimina los valores ausentes
# 
# Al trabajar con valores duplicados, pudimos observar que también nos falta investigar valores ausentes:
# 
# * La columna `'product_name'` de la tabla products.
# * La columna `'days_since_prior_order'` de la tabla orders.
# * La columna `'add_to_cart_order'` de la tabla order_productos.

# %% [markdown]
# ### `products` data frame

# %%
# Encuentra los valores ausentes en la columna 'product_name'
print('Numero de nombres ausentes: ',df_products['product_name'].isna().sum())

# %% [markdown]
# Tenemos varios nombres de productos ausentes en el dataframe con un total de 1258

# %%
#  ¿Todos los nombres de productos ausentes están relacionados con el pasillo con ID 100?
df_products_isna=df_products[df_products['product_name'].isna()]
print(df_products_isna)
#Hacemos un groupby para revisar si absolutamente todos los registros pertenecen al pasillo 100
df_products_isna.groupby('aisle_id')['aisle_id'].count()

# %% [markdown]
# 
#   Si se puede concluír que todos los ausentes están relacionados con el numero de pasillo 100

# %%
# ¿Todos los nombres de productos ausentes están relacionados con el departamento con ID 21?
#Hacemos un groupby para revisar si absolutamente todos los registros pertenecen al departamento 21
df_products_isna.groupby('department_id')['department_id'].count()

# %% [markdown]
#  
# También se puede concluír que todos los ausentes tienen que ver con el departamento 21.

# %%
# Usa las tablas department y aisle para revisar los datos del pasillo con ID 100 y el departamento con ID 21.
print(df_aisles[df_aisles['aisle_id']==100])
print(df_departments[df_departments['department_id']==21])

# %% [markdown]
#  
#   El departamento 21 y el pasillo 100 hace parte a la categoría 'missing', es decir que no tienen departamento ni pasillo aisgnado. 

# %%
# Completa los nombres de productos ausentes con 'Unknown'
df_products['product_name'].fillna('Unknown',inplace=True)
print(df_products.isna().sum())

# %% [markdown]
# 
#   Al reemplazar 'Unknown' en los nombres de los productos ausentes, podemos descartar estos para el análisis.

# %% [markdown]
# ### `orders` data frame

# %%
# Encuentra los valores ausentes
print(df_instacart.isna().sum())

# %%
# ¿Hay algún valor ausente que no sea el primer pedido del cliente?
columns=['order_id', 'user_id', 'order_number']
#Se usa un for para revisar si hay valor cero en los id
for column in columns:
    print(df_instacart[df_instacart[column]==0])

# %% [markdown]
# 
#   Al revisar los ausentes, no se ve ningún ausente en el dataframe de ordenes o valor extraño.

# %% [markdown]
# ### `order_products` data frame

# %%
# Encuentra los valores ausentes
print(df_order_products.isna().sum())

# %%
# ¿Cuáles son los valores mínimos y máximos en esta columna?
df_order_products['add_to_cart_order'].describe()

# %% [markdown]
#  
#   Podemos ver que el máximo de la columna 'add_to_cart_order' es 64 y el mínimo es 1

# %%
# Guarda todas las IDs de pedidos que tengan un valor ausente en 'add_to_cart_order'
order_products_isna=df_order_products['order_id'][df_order_products['add_to_cart_order'].isna()==True].sort_values()
print(order_products_isna)

# %%
order_product_filtered=df_order_products.query('order_id in @order_products_isna').sort_values(by='order_id')
print(order_product_filtered.sample(20))

# %%
# ¿Todos los pedidos con valores ausentes tienen más de 64 productos?
df_groupby_product_id=order_product_filtered.groupby('order_id')['product_id'].count().sort_values(ascending=False)
# Agrupa todos los pedidos con datos ausentes por su ID de pedido.
print('¿Todos los pedidos con valores ausentes tienen más de 64 productos?\n',df_groupby_product_id.head(30))
print()
# Cuenta el número de 'product_id' en cada pedido y revisa el valor mínimo del conteo.
print('Máximo:',df_groupby_product_id.max(),'\nMínimo: ',df_groupby_product_id.min())

# %% [markdown]
#  
#   Podemos ver que los valores nulos son porque los la columna 'add_to_cart' solo cuenta hasta 64 valores en el carrito, quiere decir que si una orden tiene más de 64 productos, del producto 64, en adelante, el valor en esta columna será nulo. Podemos ver que las ordenes que tienen valores nulos, tienen mínimo 65 productos y maximo 127 productos, esto prueba nuestro argumento de porque se presentan nulos en esta columna.

# %%
# Remplaza los valores ausentes en la columna 'add_to_cart_order' con 999 y convierte la columna al tipo entero.
df_order_products['add_to_cart_order'].fillna(999,inplace=True)
print(df_order_products['add_to_cart_order'].isna().sum())

# %% [markdown]
# Describe brevemente tus hallazgos y lo que hiciste con ellos.   
#   Al rellenar los valores de la columna 'add_to_cart_order' con 999 sabemos que es un valor en el carrito posterior al producto 64.

# %% [markdown]
# ## Conclusiones
# 
# Paso 2. Preprocesamiento de los datos
# 
# En conclusión los valores duplicados de los dataframes son normales a excepción del dataframe 'products', que tiene nombres repetidos para varios id de producto, y el dataframe instacart, debido a que teniamos líneas repetidas para varios pedidos del miércoles a las 2 am.
# 
# Los ausentes importantes que arreglamos fueron los de los dataframes products y order_products, donde en el dataframe products tenemos valores ausentes en los nombres, los cuales reemplazamos por el nombre 'Unknown' para diferenciarlos. Por otro lado en el dataframe 'order_products' reemplazamos los ausentes por '999' debido a que son ordenes que exceden los 64 productos y no están mapeados en el dataframe. 
# 

# %% [markdown]
# # Paso 3. Análisis de los datos
# 

# %% [markdown]
# ### [A1] Verifica que los valores sean sensibles

# %%
print('Análisis order_hour_of_day:n',df_instacart['order_hour_of_day'].describe())
print('\nAnálisis order_dow:\n',df_instacart['order_dow'].describe())

# %% [markdown]
# Escribe aquí tus conclusiones  
#   **Los datos de 'order_hour_of_day' oscilan entre 0 y 23, mientras que 'order_dow' oscila entre 0 y 6 como lo vemos en los análisis estadisticos.**

# %% [markdown]
# ### [A2] Para cada hora del día, ¿cuántas personas hacen órdenes?

# %%
#Función para agregar etiquetas de datos
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center')

# %%

df_a2=df_instacart.groupby('order_hour_of_day')['order_id'].count().reset_index()
df_a2.sort_values(by='order_hour_of_day',inplace=True)
df_a2.plot(kind='bar',
            x='order_hour_of_day',
            y='order_id',
            xlabel='Hora del día',
            ylabel='Número de ordenes',
            title='Número de ordenes por hora del día',
            legend=False,
           figsize=[20,10]
          )
addlabels(df_a2['order_hour_of_day'],df_a2['order_id'])
plt.show()

# %% [markdown]
# Podemos concluír que a las 10 se realizan más compras, y a las 3 se hacen menos compras.

# %% [markdown]
# ### [A3] ¿Qué día de la semana compran víveres las personas?

# %%
df_a3=df_instacart.groupby('order_dow')['order_id'].count().reset_index()
df_a3.sort_values(by='order_dow',inplace=True)
df_a3.plot(kind='bar',
            x='order_dow',
            y='order_id',
            xlabel='Día de la semana',
            ylabel='Número de ordenes',
            title='Número de ordenes por día',
            legend=False,
          )
addlabels(df_a3['order_dow'],df_a3['order_id'])
plt.show()

# %% [markdown]
# Podemos concluír que los domingos y los lunes son los días que más viveres se compran, y el día jueves es el día en que menos compras se hacen.

# %% [markdown]
# ### [A4] ¿Cuánto tiempo esperan las personas hasta hacer otro pedido? Comenta sobre los valores mínimos y máximos.

# %%
df_instacart['days_since_prior_order'].describe()

# %%
df_instacart['days_since_prior_order'].plot(kind='hist',
                                            title='Tiempo de espera para hacer un nuevo pedido',
                                            bins=30
                                           )


# %% [markdown]
# Las personas suelen tomar con más frecuencia 30 días para hacer un nuevo pedido, seguido de 7 días para hacer un pedido, y las personas toman con menos frecuencia 27 días para hacer una nueva compra.

# %% [markdown]
# <div class="alert alert-block alert-success">
# <b>Comentario del revisor</b> <a class="tocSkip"></a>
#     
# Muy buen trabajo en esta sección.
# </div>

# %% [markdown]
# ### [B1] Diferencia entre miércoles y sábados para  `'order_hour_of_day'`. 

# %%
df_instacart[df_instacart['order_dow'] == 3]['order_hour_of_day'].plot(kind='hist', bins=20,alpha=0.5)
df_instacart[df_instacart['order_dow'] == 6]['order_hour_of_day'].plot(kind='hist', bins=20,alpha=0.3)
plt.legend(['miercoles','sabado'])
plt.title('Distribuciones de horas de compra miercoles vs sabado')

plt.show()


# %%
df_b1=df_instacart.groupby(df_instacart[df_instacart['order_dow'] == 3]['order_hour_of_day'])['order_id'].count().reset_index()
df_b11=df_instacart.groupby(df_instacart[df_instacart['order_dow'] == 6]['order_hour_of_day'])['order_id'].count().reset_index()
df_columns=df_b1.merge(df_b11,on='order_hour_of_day')
df_columns.columns=['order_hour_of_day','miercoles','sabado']
df_columns

# %%

df_columns.plot(kind='bar', 
           x='order_hour_of_day',
           y=['miercoles','sabado'],
           xlabel='Horas de compra',
           ylabel='Número de compras',
           title='Distribución de compras el día miercoles y sábado',
            figsize=[10,5])
plt.show()

# %% [markdown]
# Podemos ver que las distribuciones de compras entre el miercoles y el sabado son similares, sin embargo, varían entre las 12 del medio día y las 2pm, debido a que esas horas es cuando más compras hay los sabados, en cambio, los miercoles a las 10am se aumentan las compras, después de las 11am disminuyen y a las 3pm vuelven a aumentar. 

# %% [markdown]
# ### [B2] ¿Cuál es la distribución para el número de pedidos por cliente?

# %%
df_instacart['order_number'].plot(kind='hist',
                                bins=20,
                                title='Distribución de numero de pedidos'
                                 )
plt.show()

# %% [markdown]
# Podemos ver que la distribución es de una frecuencia mayor al ser la primera compra, y va disminuyendo periodicamente a medida que aumenta el numero de pedidos.

# %% [markdown]
# ### [B3] ¿Cuáles son los 20 productos más populares (muestra su ID y nombre)?

# %%
df_most_popular=df_order_products.merge(df_products,on='product_id')
df_most_popular.head(10)

# %%
df20_most_popular=df_most_popular.groupby(['product_id','product_name'])['order_id'].count().sort_values(ascending=False)
df20_most_popular1=df20_most_popular.head(20)
df20_most_popular1

# %%
ax = df20_most_popular1.plot.barh(x='product_name', y='order_id')
plt.title('Top 20')
plt.xlabel('Numero de compras')
plt.ylabel('Nombre de producto')
ax.invert_yaxis()
plt.show()

# %% [markdown]
# Podemos ver en el siguiente gráfico, los 20 productos más populares, destacando la banana de primero, la bolsa de bananas organicas de segundo y la fresa organica de tercero.

# %% [markdown]
# ### [C1] ¿Cuántos artículos compran normalmente las personas en un pedido? ¿Cómo es la distribución?

# %%
df_order_products['add_to_cart_order']=df_order_products['add_to_cart_order'].astype('int')
df_order_products1=df_order_products[df_order_products['add_to_cart_order']!=999]
df_order_products2=df_order_products1.groupby('order_id')['add_to_cart_order'].max().sort_values(ascending=False)
df_order_products2.head(10)
print('En promedio se compran ',df_order_products2.mean().round(0),' arrticulos.')

# %%
df_order_products2.plot(kind='hist',
                       bins=20,
                       title='Distribución de número de productos por pedido')
plt.show()

# %% [markdown]
# Podemos concluír que se compran en promedio 10 productos por pedido, y a su distribución va disminuyendo a medida que la cantidad de productos aumenta.

# %% [markdown]
# ### [C2] ¿Cuáles son los 20 principales artículos que vuelven a pedirse con mayor frecuencia?

# %%
df_reordered_most_popular=df_most_popular[df_most_popular['reordered']==1]
df_reordered_most_popular.head(10)

# %%
df20_reordered_most_popular=df_reordered_most_popular.groupby(['product_id','product_name'])['order_id'].count().sort_values(ascending=False)
df20_reordered_most_popular1=df20_reordered_most_popular.head(20)
df20_reordered_most_popular1

# %%
ax = df20_reordered_most_popular1.plot.barh(x='product_name', y='order_id')
plt.title('Top 20')
plt.xlabel('Numero de compras')
plt.ylabel('Nombre de producto')
ax.invert_yaxis()
plt.show()

# %% [markdown]
# Se puede evidenciar en la anterior gráfica que los 20 productos que más se reordenan, comenzando con la banana de primero, posteriormente la bolsa de bananas de segundo y la fresa organica de tercero. Si comparamos este top 20 con el primero top 20 que se realizó con los productos en general, vemos un producto que no aparecen en el top general, como lo es el Medio y medio organico.

# %% [markdown]
# ### [C3] Para cada producto, ¿cuál es la proporción de las veces que se pide y que se vuelve a pedir?

# %%
df20_reordered_most_popular1=df20_reordered_most_popular.reset_index()
df20_most_popular1=df20_most_popular.reset_index()
df_proporcion=df20_most_popular1.merge(df20_reordered_most_popular1,on='product_id')
df_proporcion.drop('product_name_y',axis=1,inplace=True)
df_proporcion['proporcion']=(df_proporcion['order_id_y']/df_proporcion['order_id_x'])
df20_proporcion=df_proporcion.head(20)
df20_proporcion

# %%
df20_proporcion.plot(kind='bar',
                  x='product_name_x',
                  y='proporcion',
                  xlabel='Nombre de producto',
                  ylabel='Proporción',
                  title='Porcentaje de productos reordenados',
                  rot=90
                    )

plt.show()

# %% [markdown]
# Podemos ver en la anterior tabla la proporción que tiene cada producto en ser reordenado, en la columna 'porporcion, adicionalmente, podemos ver en la anterior gráfica, la tasa de reordenamiento de los 20 productos más populares, destacando con una tasa de reordenamiento alta para las bananas, la bolsa de bananas organicas y la leche entera organica.

# %% [markdown]
# ### [C4] Para cada cliente, ¿qué proporción de sus productos ya los había pedido?

# %%
df_clients=df_order_products.merge(df_instacart,on='order_id')
df_clients_order=df_clients.groupby('user_id', as_index=False)['order_id'].count().sort_values(by='order_id',ascending=False)
df_clients_reordered=df_clients[df_clients['reordered']==1]
df_clients_reordered1=df_clients_reordered.groupby('user_id',as_index=False)['order_id'].count().sort_values(by='order_id',ascending=False)

# %%
df_proporcion2=df_clients_order.merge(df_clients_reordered1,on='user_id')
df_proporcion2['proporcion']=(df_proporcion2['order_id_y']/df_proporcion2['order_id_x'])
df20_proporcion2=df_proporcion2.head(20)
df20_proporcion2

# %%
df20_proporcion2.plot(kind='bar',
                  x='user_id',
                  y='proporcion',
                  xlabel='ID del usuario',
                  ylabel='Proporción',
                  title='Porcentaje de productos reordenados por cliente',
                  rot=90,
                  legend=False
                    )

plt.show()

# %% [markdown]
# Podemos ver en la anterior tabla la proporción que tienen los productos de cada cliente en ser reordenados, en la columna 'porporcion', adicionalmente, podemos ver en la anterior gráfica, la tasa de reordenamiento de los 20 clientes que más compras tienen, destacando con una tasa de reordenamiento alta para el cliente 23832 con tasa de 94%.

# %% [markdown]
# ### [C5] ¿Cuáles son los 20 principales artículos que las personas ponen primero en sus carritos?

# %%
df_most_popular_first=df_most_popular[df_most_popular['add_to_cart_order']==1]
df20_most_popular_first=df_most_popular_first.groupby(['product_id','product_name'])['order_id'].count().sort_values(ascending=False)
df20_most_popular_first=df20_most_popular_first.head(20)
df20_most_popular_first

# %%
ax = df20_most_popular_first.plot.barh(x='product_name', y='order_id')
plt.title('Top 20 primeros artículos')
plt.xlabel('Numero de compras')
plt.ylabel('Nombre de producto')
ax.invert_yaxis()
plt.show()

# %% [markdown]
# Se puede evidenciar en la anterior gráfica los 20 articulos principales que los clientes ordenan de primero en sus carritos, destacando las bananasm la bolsa de bananas organica y la leche entera organica.

# %% [markdown]
# ### Conclusion general del proyecto:

# %% [markdown]
# En general, podemos concluír que los productos como las bananas, la bolsa organica de bananas, lasfresas organicas y la leche entera organica, se repiten siendo parte de los 20 productos más populares, los 20 articulos que más se reordenan y los 20 productos que se eligen de primero en sus carritos, entre otros más que se repiten en en esta recompilación, por lo cual pueden considerarse productos básicos.
# 
# Adicionalmente, se puede considerar que estos productos se reordenan constantemente, viendo su proporción de reordenamiento, debido a que en la mayoría de las ocasiones, más del 80% se termina reordenando.
# 
# Los clientes que más compras tienen también tienden a reordenar sus productos, del total mas del 80% de productos se reordenan, por lo cual se cuenta con una fidelizaón del cliente alta.
# 
# Con respecto a la cantidad de productos que se piden por orden, podemos ver que con frecuencia se piden entre 0 a 10 productos, y va disminuyendo a medida que aumenta el numero de productos.
# 
# Los días que más compras se realizan son los domingos y los lunes, las horas donde más se compra son entre las 2pm y las 3pm, y los clientes generalmente compran cada 30 dias.


