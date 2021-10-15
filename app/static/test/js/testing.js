function choose(test_id , question_id , value){
    url='/check/'
    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({
            'test_id':test_id,
            'question_id':question_id,
            'value':value})
        })
        .then((response)=>{
        response.json().then((data) => {
            console.log(data)
        })
    }) 
}
function finish(test_id){
    console.log(test_id)
    url='/result/'
    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'test_id':test_id})
    }).then((response)=>{
        response.json().then((data) => {
            window.location.replace(`/scores/${test_id}`);
        })
    }) 
}
function checked(id){
    console.log(id)
    id = 'q'+id
    item = document.getElementById(id)
    item.style.backgroundColor = 'blue'
    item.style.color = 'white'
}
document.addEventListener('DOMContentLoaded', () => {
    const timeLeftDisplay = document.querySelector('#time-left');
    const startbtn = document.querySelector('.start-button');
    let timeLeft = 30;

    function countDown() {
        setInterval(function () {
            if (timeLeft < 0) {
                clearInterval(timeLeft = -1)
            }
            if (timeLeft == 0) {
                $("#questions").hide();
                $("#answer-sheet").hide();
                let a = document.getElementById('questions')
                console.log(a.dataset.id)
                finish(a.dataset.id)
            }
            timeLeftDisplay.innerHTML = timeLeft
            timeLeft--;
        }, 1000)
    }
    startbtn.addEventListener('click', countDown)
});
function start(){
    document.getElementById('questions').style.display = 'block'
    document.getElementById('answer-sheet').style.display = 'block'
}

function practice_test(subject_id){
    console.log(subject_id)
    url=`/practice_test/`
    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({
            'subject_id':subject_id,
        })
        })
        .then((response)=>{
        response.json().then((data) => {
            console.log(data)
            //  html = ''
            // document.getElementById('subject_test').innerHTML = html
        })
    })
}
window.onload=function()
{
    document.getElementById("select").onchange=function()
    {console.log('print print print')
        if(this.options[this.selectedIndex].value!='')
        {
            document.getElementById("btnSubmit").disabled=false;
        }
        // else
        // {
        //     document.getElementById("submit-button").disabled=false;
        // }
    }
}

function change(id){
    console.log(id)
    url=`/changestatus/`
    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({
            'user_id':id,
        })
    })
}


// function attempt(id) {
//     url = '/start'
//     fetch(url, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrftoken,
//         },
//         body: JSON.stringify({
//             'id': id
//         })
//     })
//         .then((response) => {
//             response.json().then((data) => {
//                 console.log(data)
//                 document.getElementsByClassName('total-count')[0].innerHTML = data.count
//             })
//         })
// }