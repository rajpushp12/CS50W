document.addEventListener('DOMContentLoaded', function(){


    var btn1=document.querySelector('#follow-btn');
    btn1.onclick = () => connections_add(btn1.value);

    var btn2=document.querySelector('#unfollow-btn');
    btn2.onclick = () => connections_remove(btn2.value);

    btn();

});

function btn(){
    document.querySelector('#follow-btn').style.display = 'block';
    document.querySelector('#unfollow-btn').style.display = 'none';
}

function connections_add(name){

    console.log(`${name}`);

    fetch(`/connect_fetch/${name}`)
    .then(response => response.json())
    .then(like => {

        console.log(like.followers_count);
        
        const count=like.followers_count;
        document.querySelector('#count').innerHTML = `${count+1} Followers`;

        fetch(`/connect_add/${name}` ,{
            method: 'PUT'
        })
    });
    document.querySelector('#follow-btn').style.display = 'none';
    document.querySelector('#unfollow-btn').style.display = 'block';
}


function connections_remove(name){

    fetch(`/connect_fetch/${name}`)
    .then(response => response.json())
    .then(like => {

        console.log(like.followers_count);

        const count=like.followers_count;
        document.querySelector('#count').innerHTML = `${count-1} Followers`;

        fetch(`/connect_remove/${name}` ,{
            method: 'PUT'
        })
    });
    document.querySelector('#follow-btn').style.display = 'block';
    document.querySelector('#unfollow-btn').style.display = 'none';
}

