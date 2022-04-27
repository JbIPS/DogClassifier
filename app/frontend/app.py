import streamlit as st
import requests


def request_prediction(model_uri, data):
    payload = {'q': data}
    response = requests.get(url=model_uri, params=payload)

    if response.status_code != 200:
        raise Exception(
            "Request failed with status {}, {}".format(
                response.status_code, response.text))

    return response.json()


def main():
    API_URI = 'http://backend:8000/prediction'

    st.set_page_config("Who let's the dogs out")
    st.title('Quelle est ta race de chien totem ?')

    st.text('''
    Pour découvrir ta race de chien, colle l'adresse d'une photo.
    ''')
    url = st.text_input('URL de la photo')
    predict_btn = st.button('Prédire')
    if predict_btn:
        pred = request_prediction(API_URI, url)
        main_race = pred[0].split(' at')[0].lower()
        main_race = '/'.join(reversed(main_race.replace('-', '').split(' ')))
        if main_race.startswith('husky'):
            main_race = main_race.split('/')[0]
        col1, col2 = st.columns(2)
        with col1:
            st.image(url)
        with col2:
            response = requests.get(url=f'https://dog.ceo/api/breed/{main_race}/images/random').json()
            if response['status'] == 'success':
                st.image(response['message'])
            else:
                st.text(main_race)
                st.text(response)
        st.write('Les races qui te correspondent le plus sont :')
        for race in pred:
            st.write(race)


if __name__ == '__main__':
    main()
