document.addEventListener('DOMContentLoaded', function(){
    document.querySelectorAll('#edit-btn').forEach(function(button){
        button.onclick = () => edit_load(button.value);
    });

    //Default
    index_load();
});



function index_load() {
    document.querySelector('#index-view').style.display = 'block';
    document.querySelector('#edit-view').style.display = 'none';
}



function edit_load(id) {
    document.querySelector('#index-view').style.display = 'none';
    document.querySelector('#edit-view').style.display = 'block';

    fetch(`/post/${id}`)
    .then(response => response.json())
    .then(post => {
        console.log(post);

        document.querySelector('#edit-body').innerHTML = post.post_content;
    });
    document.querySelector('#edit-form').onsubmit = post_update(id);
}



function post_update(id){
    const content = document.querySelector('#edit-body').value
    fetch(`/post/${id}` ,{
        method: 'PUT',
        body: JSON.stringify({
            post_content: content
        })
    })
    return false;
}