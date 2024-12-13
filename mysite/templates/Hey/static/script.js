// script.js

function initializeJitsi() {
    // Change the domain to your own Jitsi server or a suitable public server.
    const domain = 'meet.jit.si'; // Update this

    const options = {
        roomName: 'YourUniqueRoomName',
        width: '100%',
        height: '800px',
        configOverwrite: {
            prejoinPageEnabled: false,
            disableInviteFunctions: true,
            disableChat: true,
            toolbarButtons: [],
        },
        interfaceConfigOverwrite: {
            filmStripOnly: false,
            DEFAULT_BACKGROUND: '#000000',
        },
        parentNode: document.querySelector('#meet'),
    };
    const api = new JitsiMeetExternalAPI(domain, options);

    // Language translation using Google Translate API
    const googleTranslateApiKey = 'AIzaSyCitHDWcwBdBGNuPs9ICojg9Y-rQNXIOcA';
    const translateEndpoint = 'https://translation.googleapis.com/language/translate/v2';

    // Chat log array
    let chatLog = [];

    function detectLanguage(message) {
        const url = `${translateEndpoint}/detect?key=${googleTranslateApiKey}&q=${encodeURIComponent(
            message
        )}`;

        return fetch(url)
            .then((response) => response.json())
            .then((data) => {
                const detectedLanguage = data.data.detections[0][0].language;
                return detectedLanguage;
            })
            .catch((error) => console.log(error));
    }

    function translateMessage(message, targetLanguage) {
        return detectLanguage(message)
            .then((sourceLanguage) => {
                const url = `${translateEndpoint}?key=${googleTranslateApiKey}&q=${encodeURIComponent(
                    message
                )}&source=${sourceLanguage}&target=${targetLanguage}`;

                return fetch(url)
                    .then((response) => response.json())
                    .then((data) => {
                        const translatedText = data.data.translations[0].translatedText;
                        displayTranslatedMessage(message, translatedText, targetLanguage);
                    })
                    .catch((error) => console.log(error));
            });
    }

    function addToChatLog(originalMessage, translatedMessage, targetLanguage) {
        const user = api._displayName; // Get the user's display name from Jitsi Meet API
        const chatEntry = {
            user,
            originalMessage,
            translatedMessage,
            targetLanguage,
            timestamp: new Date().toISOString(),
        };
        chatLog.push(chatEntry);
        console.log(chatLog); // You can inspect the chat log in the browser console
    }

    function displayTranslatedMessage(originalMessage, translatedMessage, targetLanguage) {
        const messagesDiv = document.querySelector('#messages');
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.innerHTML = `
            <strong>Original (${targetLanguage}):</strong> ${originalMessage}<br>
            <strong>Translated (${targetLanguage}):</strong> ${translatedMessage}<br>
        `;
        messagesDiv.appendChild(messageElement);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }
    
    

    // Chat functionality
    function sendMessage() {
        const inputElement = document.querySelector('#messageInput');
        const message = inputElement.value.trim();

        if (message !== '') {
            // Translate and display the message for each language
            const languages = ['en', 'fr', 'es', 'uk']; // Replace with desired languages

            const translationPromises = languages.map((language) => {
                return translateMessage(message, language);
            });

            Promise.all(translationPromises)
                .then(() => {
                    inputElement.value = ''; // Clear input field
                })
                .catch((error) => console.log(error));
        }
    }

    // Expose the sendMessage function globally
    window.sendMessage = sendMessage;
}

function loadJitsiMeetAPI() {
    const script = document.createElement('script');
    script.src = 'https://meet.jit.si/external_api.js';
    script.async = true;
    script.onload = initializeJitsi;
    document.body.appendChild(script);
}

loadJitsiMeetAPI();

// Reload the Jitsi iframe every 4 minutes (240,000 milliseconds)
setInterval(function () {
    var iframe = document.getElementById('jitsi-iframe');
    iframe.src = iframe.src;
  }, 240000);

  

const messageInput = document.getElementById("messageInput");
const messagesDiv = document.getElementById("messages");
const languageSelect = document.getElementById("languageSelect");

function sendMessage() {
    const message = messageInput.value;
    const selectedLanguage = languageSelect.value;

    // Append the message to the messagesDiv
    const messageElement = document.createElement("div");
    messageElement.textContent = message;
    messagesDiv.appendChild(messageElement);

    // Hide other translations and show the selected translation
    const translations = document.querySelectorAll(".translation");
    translations.forEach((translation) => {
        if (translation.id === selectedLanguage) {
            translation.style.display = "block";
        } else {
            translation.style.display = "none";
        }
    });

    // Scroll to the bottom of the messagesDiv
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    // Clear the message input
    messageInput.value = "";
}
