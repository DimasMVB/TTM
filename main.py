
import streamlit as st
import groq
Modelos = ['llama3-8b-8192', 'llama3-70b-8192','mixtral-8x7b-32768']

st.set_page_config(page_title="Clase Python")

def configurar_pagina():
 st.title("TTM")
 


def mostrar_sidebar():
    st.sidebar.title("Elegi tu IA")
    modelo = st.sidebar.selectbox("Elegi tu modelo", Modelos, index = 0)
    st.header(f"**Elegiste el modelo** {modelo}")
    return modelo

def mostrar_mensajes(role, content):
    with st.chat_message(role):
     st.markdown(content)

def crear_cliente_groq():
    groq_api_key = st.secrets["GROQ_API_KEY"]
    return groq.Groq(api_key = groq_api_key)

def obtener_mensaje_usuario():
    return st.chat_input("Envia tu mensaje")

def inicializar_estado_chat():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []
        
def ejecutar_chat():
    configurar_pagina()
    cliente = crear_cliente_groq()
    modelo = mostrar_sidebar()
    inicializar_estado_chat()
    obtener_mensajes_previos()
    mensaje_usuario = obtener_mensaje_usuario()
    print(mensaje_usuario)
    
    
    
    if mensaje_usuario:
        agregar_mensajes_previos("user", mensaje_usuario)
        mostrar_mensajes("user", mensaje_usuario)
        
        respuesta_contenido = obtener_respuesta_modelo(cliente, modelo, st.session_state.mensajes)
        
        agregar_mensajes_previos("assistant",respuesta_contenido)
        mostrar_mensajes("assistant",respuesta_contenido)
    


    

    

def agregar_mensajes_previos(role, content):
    st.session_state.mensajes.append({"role": role , "content": content})

def obtener_mensajes_previos():
    for mensaje in st.session_state.mensajes: # recorrer los mensajes de st.session_state.mensaje
        with st.chat_message(mensaje['role']): #quien lo envia ??
         st.markdown(mensaje["content"]) #que envia?

def obtener_respuesta_modelo(cliente,modelo,mensaje):
    respuesta = cliente.chat.completions.create(
        model = modelo,
        messages = mensaje,
        stream = False
    )
    return respuesta.choices[0].message.content


        

if __name__ == '__main__':
    ejecutar_chat()
    


