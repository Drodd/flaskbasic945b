       const startButton = document.getElementById('startButton');
        const audioPlayer = document.getElementById('audioPlayer');

        startButton.addEventListener('click', async () => {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                const recorder = new MediaRecorder(stream);
                const audioChunks = [];

                recorder.addEventListener('dataavailable', (event) => {
                    audioChunks.push(event.data);
                });

                recorder.addEventListener('stop', async () => {
                    const audioBlob = new Blob(audioChunks);
                    const formData = new FormData();
                    formData.append('audio', audioBlob, 'recording.wav');

                    const response = await fetch('/chat', {
                        method: 'POST',
                        body: formData
                    });

                    const audioData = await response.blob();
                    audioPlayer.src = URL.createObjectURL(audioData);
                    audioPlayer.play();
                });

                recorder.start();
                startButton.textContent = '停止说话';
                startButton.addEventListener('click', () => {
                    recorder.stop();
                    startButton.textContent = '开始说话';
                }, { once: true });
            } catch (error) {
                console.error('Error recording audio:', error);
            }
        });
