document.addEventListener('DOMContentLoaded', function(){

    document.querySelectorAll('#edit-btn').forEach(function(button){
        button.onclick = () => edit_load(button.value);
    });

    document.querySelectorAll('#like-btn').forEach(function(button){
        button.onclick = () => like_update(button.value, button);
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

    document.querySelector('#edit-form').onsubmit = () => post_update(id);
}



function post_update(id){
    const content = document.querySelector('#edit-body').value;
    console.log(content);

    fetch(`/post/${id}` ,{
        method: 'PUT',
        body: JSON.stringify({
            post_content: content
        })
    });
    document.querySelector(`#body${id}`).innerHTML = `${content}`;
    document.querySelector('#index-view').style.display = 'block';
    document.querySelector('#edit-view').style.display = 'none';
    console.log('here');
    return false;
}


function like_update(id, button){

    if(button.innerHTML==='Like'){
    fetch(`/like/${id}`)
    .then(response => response.json())
    .then(post => {

        console.log(post);
        var count=post.like_count;
        
        fetch(`/like/${id}` ,{
            method: 'PUT',
            body: JSON.stringify({
                like_count: count+1
            })
        })
        document.querySelector(`#count${id}`).innerHTML = `${count+1} Likes`;
    });
    button.innerHTML="Unlike";
    }


    else{
    fetch(`/like/${id}`)
    .then(response => response.json())
    .then(post => {

        console.log(post);
        var count=post.like_count;
        
        fetch(`/like/${id}` ,{
            method: 'PUT',
            body: JSON.stringify({
                like_count: count-1
            })
        })
        document.querySelector(`#count${id}`).innerHTML = `${count-1} Likes`;
    });
    button.innerHTML="Like";
    }
}



