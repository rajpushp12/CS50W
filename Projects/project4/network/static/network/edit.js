document.addEventListener('DOMContentLoaded', function(){
    document.querySelector('#edit-btn').addEventListener('click', () => edit_load());
});

function edit_load() {
    document.querySelector('#index-view').style.display = 'none';

}