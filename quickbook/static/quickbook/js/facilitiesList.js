document.addEventListener('DOMContentLoaded', function () {
    const today = new Date();
    const formattedDate = today.toISOString().split('T')[0];
    document.getElementById('date').value = formattedDate;
    const checkSlotsButtons = document.querySelectorAll('.check-slots');

    checkSlotsButtons.forEach(button => {
        button.addEventListener('click', function () {
            const facilityId = button.getAttribute('data-facility-id');
            const date = document.getElementById('date').value;

            fetch(`/facilities/${facilityId}/?date=${date}`)
                .then(response => response.json())
                .then(data => {
                    const slotsList = document.getElementById('slots-list');
                    slotsList.innerHTML = '';

                    if (data.slots.length > 0) {
                        data.slots.forEach(slot => {
                            const listItem = document.createElement('li');
                            listItem.classList.add('list-group-item');
                            listItem.textContent = `${slot.start_time} — ${slot.end_time}  |  Available Seats: ${slot.available_capacity}`;
                            slotsList.appendChild(listItem);
                        });
                    } else {
                        const listItem = document.createElement('li');
                        listItem.classList.add('list-group-item', 'text-danger');
                        listItem.textContent = 'No slots available';
                        slotsList.appendChild(listItem);
                    }
                })
                .catch((e) => {
                    console.log(e);
                    alert('Error fetching slots');
                });
        });
    });
});
