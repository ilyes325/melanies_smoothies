# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col 

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title("Customize your Smoothie ! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie !")

name_on_order =  st.text_input(' Name on Smoothie : ')
st.write('The name on you Smoothie will be : ', name_on_order)


cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)
ingredient_list = st.multiselect('Choose up to 5 ingredients: ', my_dataframe,max_selections=5)

# st.write("You can only select up to 5 options. Remove an option first")
if ingredient_list :
    
    ingredient_string= ''
    for fruit in ingredient_list:
        ingredient_string += fruit+' '
    # st.write(ingredient_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredient_string +"""','"""+name_on_order+ """')""" 

    # st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
