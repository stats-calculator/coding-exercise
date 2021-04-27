(() => {
    window.addEventListener('DOMContentLoaded', () => {
        const showStats = stats => {
            document.getElementById('count').innerText = stats.count === undefined ? '' : stats.count;
            document.getElementById('mean').innerText = stats.mean === undefined ? '' : stats.mean;
            document.getElementById('standard-deviation').innerText = stats.sd === undefined ? '' : stats.sd;
        };

        const submitNumber = (number, userName) => {
            fetch('api/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                  number,
                  userName
              }),
            })
            .then(response => response.json())
            .then(stats => showStats(stats))
            .catch(console.error);
        };

        const reset = (userName) => {
            fetch('api/reset', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({userName})
            })
            .then(response => response.json())
            .then(stats => showStats(stats))
            .catch(console.error);
        };

        const poll = () => {
            fetch('api/stats',)
            .then(response => response.json())
            .then(stats => showStats(stats))
            .catch(console.error)
            .finally(() => setTimeout(poll, 3000));
        };

        // Switches from the intro form to the main page
        const activateMainForm = (userName) => {
            const mainForm = document.getElementById('main-form');
            mainForm.style.display = 'block';

            const valueInput = document.getElementById('new-value');
            valueInput.focus();

            // Customise help text!
            document.getElementById('addHelp').innerText += userName;

            mainForm.addEventListener('submit', event => {
                submitNumber(valueInput.value, userName);

                // Get ready for next number
                valueInput.focus();
                valueInput.value = '';

                event.preventDefault();
            });

            document.getElementById('reset').addEventListener('click', event => {
                reset(userName);
                valueInput.focus();
            });

            // Get initial data and start polling for changes from other users
            poll();
        };

        // To start with only the intro form is shown
        const introForm = document.getElementById('intro-form');
        introForm.addEventListener('submit', event => {
            const userName = document.getElementById('userName').value;

            introForm.style.display = 'none';
            activateMainForm(userName);

            event.preventDefault();
        });
    });
})();
