# gpt3 professional email generator by stefanrmmr - version June 2022

import os
import openai
import streamlit as st

# INITIATE connection to OpenAI GPT-3
openai.api_key = os.getenv("KEY")

# DESIGN implement changes to the standard streamlit UI/UX
st.set_page_config(page_title="streamlit_audio_recorder")
# Design move app further up and remove top padding
st.markdown('''<style>.css-1egvi7u {margin-top: -3rem;}</style>''',
    unsafe_allow_html=True)
# Design change st.Audio to fixed height of 45 pixels
st.markdown('''<style>.stAudio {height: 45px;}</style>''',
    unsafe_allow_html=True)
# Design change hyperlink href link color
st.markdown('''<style>.css-v37k9u a {color: #ff4c4b;}</style>''',
    unsafe_allow_html=True)  # darkmode
st.markdown('''<style>.css-nlntq9 a {color: #ff4c4b;}</style>''',
    unsafe_allow_html=True)  # lightmode


def gen_mail_contents(email_contents):
    # iterate through all seperate topics
    for topic in range(len(email_contents)):
        input_text = email_contents[topic]
        text_length = len(input_text)
        rephrased_content = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Rewrite the text to sound professional, polite and motivated. {input_text}\nText: \nRewritten text:",
            temperature=0,
            max_tokens=text_length,
            top_p=0.68,
            best_of=3,
            frequency_penalty=0,
            presence_penalty=0)
        # replace existing topic text with updated
        email_contents[topic] = rephrased_content
    return email_contents


def gen_mail_format(sender, recipient, contents):
    # update the contents data with more formal statements
    contents = gen_mail_contents(contents)

    contents_str, contents_length = "", 0
    for topic in contents:  # aggregate all contents into one
        contents_str = contents_str + "\nContent: " + topic
        contents_length += len(topic)  # calc total chars

    email_final_text = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Write a professional sounding email text that includes all of the following contents separately.\nThe text needs to be written to adhere to the specified writing styles and abbreviations need to be replaced.\n\nSender: {sender}\nRecipient: {recipient} {contents_str}\nWriting Styles: motivated, formal\n\nEmail Text:",
        temperature=1,
        max_tokens=100+contents_length,
        top_p=0.52,
        best_of=3,
        frequency_penalty=0,
        presence_penalty=1.4)

    return email_final_text


def main_gpt3emailgen():

    # TITLE and Creator information
    st.title('GPT-3 Professional Email Generator')
    st.markdown('Implemented by '
        '[Stefan Rummer](https://www.linkedin.com/in/stefanrmmr/) - '
        'view project source code on '
        '[GitHub](https://github.com/stefanrmmr/gpt3_mail_generator)')
    st.write('\n\n')

    input_contents = []  # let the user input all the data
    input_sender = st.text_input('Sender Name', 'your name here')
    input_recipient = st.text_input('Recipient Name', 'recipient name here')
    input_contents_1 = st.text_input('Email Content 1', 'content 1 here')
    input_contents_2 = st.text_input('Email Content 2', 'content 2 here')
    input_contents = input_contents.append(input_contents_1)
    input_contents = input_contents.append(input_contents_2)

    if st.button('Generate Email'):
        with st.spinner():
            email_text = gen_mail_format(input_sender, input_recipient, input_contents)

            st.text(email_text)  #output the results


if __name__ == '__main__':
    # call main function
    main_gpt3emailgen()
