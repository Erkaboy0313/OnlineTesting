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
function update_test(subject_id){
    console.log(subject_id)
    url=`/update_test/`
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
             html = ''
            k=0
            for (let i=0; i<data.tests.length;i++) {
                if (data.tests[i].status){
                    html += `
                         <div class="form-check form-switch">
                                  <input class="form-check-input" type="checkbox" name="switch${i+1}" value="${data.tests[i].id}" checked>
                                  <label class="form-check-label" for="flexSwitchCheckDefault">Default switch ${i+1}</label>
                              </div>
                              <textarea rows="8" cols="120">
                                  ${data.tests[i].q}
                                  a) ${data.tests[i].v1}
                                  b) ${data.tests[i].v2}
                                  c) ${data.tests[i].v3}
                                  d) ${data.tests[i].v4}
                                  Answear: ${data.tests[i].ans}
                              </textarea>
                            
                    `
            }
                else{
                    html += `
                         <div class="form-check form-switch">
                                  <input class="form-check-input" type="checkbox" name="switch${i+1}" value="${data.tests[i].id}" >
                                  <label class="form-check-label" for="flexSwitchCheckDefault">Default switch ${i+1}</label>
                              </div>
                              <textarea rows="8" cols="120">
                                  ${data.tests[i].q}
                                  a) ${data.tests[i].v1}
                                  b) ${data.tests[i].v2}
                                  c) ${data.tests[i].v3}
                                  d) ${data.tests[i].v4}
                                  Answear: ${data.tests[i].ans}
                              </textarea>
                            
                    `
                }
            }
            document.getElementById('subject_test').innerHTML = html
        })
    })
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