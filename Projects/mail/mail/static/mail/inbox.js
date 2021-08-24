document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').onsubmit = send_mail;
  
  // By default, load the inbox
  load_mailbox('inbox');
});





function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-read').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}



function send_mail(){

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  });

  load_mailbox('sent');
  return false;
}





function load_mailbox(mailbox) {

  document.querySelector('#emails-view').innerHTML = '';
  const table=document.createElement('table');
  table.className="table";
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-read').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails);

    emails.forEach( email => {

      var Tr=document.createElement('tr');
      Tr.className=email.read?"read-true":"read-false";

      if(mailbox==='sent'){
        
        Tr.innerHTML=`
        <td>${email.recipients}</td>
        <td>${email.subject}</td>
        <td>${email.timestamp}</td>
        `;

        table.appendChild(Tr);
        Tr.addEventListener('click', () => email_read(email.id, true));
      }


      else if(email.archived){

        Tr.innerHTML=`
        <td>${email.sender}</td>
        <td>${email.subject}</td>
        <td>${email.timestamp}</td>
        `;

        table.appendChild(Tr);

        Tr.addEventListener('click', () => email_read(email.id, false));
      }


      else{

        if(Tr.className==="read-true"){
          Tr.style.backgroundColor="gray";
          }

        Tr.innerHTML=`
        <td>${email.sender}</td>
        <td>${email.subject}</td>
        <td>${email.timestamp}</td>
        `;

        table.appendChild(Tr);

        Tr.addEventListener('click', () => {

          email_read(email.id, false);

          fetch(`/emails/${email.id}`, {
            method: 'PUT',
            body: JSON.stringify({
                read: true
            })
            })
        });
      }
    });
  });
  document.querySelector('#emails-view').appendChild(table);
}






function email_read(id, status) {

  document.querySelector('#email-read').innerHTML='';
  const display=document.createElement('div');
  
  // Show the mailbox and hide other views
  document.querySelector('#email-read').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    // Print email
    console.log(email);

    //setting archive variable for reference
    var button_name=email.archived?'Unarchive':'Archive';


      if(status){
        display.innerHTML=`
        <div><h4>Subject: ${email.subject}</h4></div>
        <div>To: ${email.recipients}</div>
        <div>From: ${email.sender}</div>
        <hr>
        <div>${email.timestamp}</div>
        <hr>
        <div>${email.body}</div>
        `;
      }

      else{

        display.innerHTML=`
        <div><h4>Subject: ${email.subject}</h4></div>
        <div>To: ${email.recipients}</div>
        <div>From: ${email.sender}</div>
        <hr>
        <div>${email.timestamp}</div>
        <hr>
        <div>${email.body}</div>
        <br>
        <input type="submit" id="archive_btn" class="btn btn-secondary btn-block" value=${button_name}>
        <hr>
        <input type="submit" id="reply_btn" class="btn btn-danger btn-block" value=Reply>
        `;

      }

        document.querySelector('#email-read').appendChild(display);

        document.querySelector('#reply_btn').addEventListener('click', () => reply(id));

        document.querySelector('#archive_btn').addEventListener('click', () => {

          fetch(`/emails/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
                archived: !email.archived
            })
          });
          load_mailbox('inbox');
          location.reload();
        });

    });
}


function reply(id){
  
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-read').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';


  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);

      document.querySelector('#compose-recipients').value=email.sender;
      document.querySelector('#compose-recipients').disabled=true;
      document.querySelector('#compose-subject').value=`Re: ${email.subject}`;
      document.querySelector('#compose-body').value=`On ${email.timestamp} ${email.recipients} wrote:`;
  });

  document.querySelector('#compose-form').onsubmit = send_mail;
}