import pandas as pd 
import numpy as np 
import streamlit as st
import boto3
import tempfile
import joblib

from secret import access_key, secret_access_key
import requests
from streamlit_lottie import st_lottie_spinner


st.title('Mobile Price Prediction')


col1, col2 = st.columns(2)
with col1:
   st.header(""" Connectivity""")
   bluetooth = st.checkbox("Bluetooth")
   wifi = st.checkbox("Wi-Fi")
   st.write("""-------- """)
   dual = st.checkbox("Dual Sim")
   threeg = st.checkbox("3G" )
   fourg = st.checkbox("4G")

with col2:
   st.header("Functionality")
   
   touch = st.checkbox("Touchscreen")



st.write("""##
Batter Power""")
input_battery = st.slider("Select your desired battery power",value=1000,min_value=500,max_value = 1999,step = 1 )



st.write("""## Clock Speed""")
speed = st.slider("Select your desired Clock Speed",value=1.3,min_value=0.3,max_value = 3.0,step = 0.1 )




st.write("""## Front Camera""")
fc = st.slider("Select your Front Camera MP",value=12,min_value=0,max_value = 19,step = 1 )




st.write("""## internal Memory""")
internal = st.radio("Select your desired Internal Memory:",[2,4,8,16,32,64],horizontal=True)

st.write("""## Mobile Depth""")
depth = st.slider("Select your desired Clock Speed",value=0.5,min_value=0.1,max_value = 1.0,step = 0.1 )


st.write("""## Weight of Mobile Phone""")
weight= st.slider("Select the Weight of your Phone in g",value=120,min_value=80,max_value = 200,step = 1 )


st.write("""## Number of cores of processor""")
n_cores = st.slider("Select the Number of cores of processor",value=3,min_value=1,max_value = 8,step = 1)


st.write("""## Primary Camera Megapixel """)
cam = st.slider("Select your desired megapixels",value=11,min_value=0,max_value = 20,step = 1)


st.write("""## Pixel Resolution Height""")
pixelh = st.slider("Select your Pixel Resolution Height",value=720,min_value=0,max_value = 1960,step = 1 )


st.write("""## Pixel Resolution Width""")
pixelw = st.slider("Select your desired Pixel Resolution Width",value=1080,min_value=500,max_value = 1998,step = 1 )


st.write("""## Random Access Memory in Megabytes""")
ram = st.slider("Select your desired RAM",value=512,min_value=256,max_value = 3998,step = 1 )


st.write("""## Screen Height""")
hcm = st.slider("Select your Screen Height of mobile in cm",value=6,min_value=5,max_value = 19,step =1 )


st.write("""## Screen Width""")
wcm = st.slider("Select your Screen Width of mobile in cm",value=5,min_value=0,max_value = 18,step =1)


st.write("""## Battery Talk Time""")
talk = st.slider("Select your Battery Talk Time in hours",value=12,min_value=2,max_value = 20,step = 1)


predict_bt = st.button('Predict')




def convert_bool_to_int(lst):
    for i in range(len(lst)):
        if type(lst[i]) == bool:
            lst[i] = int(lst[i])
    return lst



def make_prediction():
    # connect to s3 bucket with the access and secret access key
    client = boto3.client(
        's3', aws_access_key_id=st.secrets["access_key"],aws_secret_access_key=st.secrets["secret_access_key"],region_name='ap-south-1')

    bucket_name = "mobilepriceprediction"
    key = "fff.pickle"

    # load the model from s3 in a temporary file
    with tempfile.TemporaryFile() as fp:
        # download our model from AWS
        client.download_fileobj(Fileobj=fp, Bucket=bucket_name, Key=key)
        # change the position of the File Handle to the beginning of the file
        fp.seek(0)
        # load the model using joblib library
        model = joblib.load(fp)

    # prediction from the model, returns 0 or 1
    return model.predict(profile_to_predict_df) 


@st.cache_data
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_loading_an = load_lottieurl(
    'https://assets6.lottiefiles.com/packages/lf20_t9gkkhz4.json')


columns1 = ["battery_power"	,"blue",	"clock_speed",	"dual_sim","fc"	,"four_g",	"int_memory",	"m_dep",	"mobile_wt",	"n_cores",	"pc"	,"px_height",	"px_width"	,"ram"	,"sc_h"	,"sc_w",	"talk_time",	"three_g"	,"touch_screen"	,"wifi"]


if predict_bt:
    inputs = [input_battery, bluetooth, speed, dual, fc, fourg,
         internal, depth, weight, n_cores, cam, pixelh,
         pixelw, ram, hcm, wcm, talk, threeg,
         touch, wifi]
    inputs = convert_bool_to_int(inputs)

    profile_to_predict_df = pd.DataFrame([inputs],columns= columns1)
    print(profile_to_predict_df)
    
    # will run the animation as long as the function is running, if final_pred exit, then stop displaying the loading animation
    # with st_lottie_spinner(lottie_loading_an, quality='high', height='200px', width='200px'):
    final_pred = make_prediction()
    print(final_pred)
    # the prediction is 0
    price = {0:{"Low"},1:{"Medium"},2:{"High"},3:{"Very High"}}
   
    if final_pred == 0:
         st.success("Congrats: Your Phones cost is Low")
    elif final_pred == 1:
         st.success("Congrats: Your Phones cost is Medium")
    
    elif final_pred == 2:
         st.success("Congrats: Your Phones cost is High")
    
    elif final_pred == 3:
         st.success("Congrats: Your Phones cost is Very High")
    
    else:
        print("Invalid value")
        # st.success("Congrats: Your Phones cost is" + cost)
 