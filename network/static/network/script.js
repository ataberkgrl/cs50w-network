document.querySelectorAll(".edit-button").forEach((button) => {
    button.addEventListener("click", () => {
        if (button.textContent == "Edit")
        {
            var editArea = document.createElement("textarea")
            editArea.classList.add("editArea")
            editArea.innerHTML = button.parentElement.querySelector(".content").innerHTML
            button.parentElement.querySelector(".content").outerHTML = editArea.outerHTML;
            button.textContent = "Save"
        }
        else if (button.textContent == "Save")
        {
            post_id = button.parentElement.dataset.postid;
            var newContent = button.parentElement.querySelector(".editArea").value;
            fetch('/', {
                method: 'EDIT',
                body: JSON.stringify({
                    "post_id": post_id,
                    "new_content": newContent
                }),
                "credentials": "include",
                headers: {
                    "x-CSRFToken": getCookie("csrftoken"),
                    "Accept": "application/json",
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (response.status == 204) {
                    var newContentNode = document.createElement("p");
                    newContentNode.classList.add("content");
                    newContentNode.innerHTML = newContent;
                    button.parentElement.querySelector(".editArea").outerHTML = newContentNode.outerHTML;
                    button.textContent = "Edit"
                }
            })
        }
    })
})

document.querySelectorAll(".likes").forEach((button) => {
    button.addEventListener("click", () => {
        post_id = button.parentElement.parentElement.dataset.postid;
        fetch('/', {
            method: 'LIKE',
            body: JSON.stringify({
                "post_id": post_id,
            }),
            "credentials": "include",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Accept": "application/json",
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.status == 204) {
                button.querySelector(".like-count").innerHTML = response.headers.get("like_count")
                button.querySelector(".heart").classList.toggle("liked");
            }
        })
    })
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.querySelector("#follow-button").addEventListener("click", () => {
    followed_name = document.querySelector("#profile-username").innerHTML
    fetch('/profile/' + followed_name, {
        method: 'FOLLOW',
        body: JSON.stringify({
            "followed_name": followed_name,
        }),
        "credentials": "include",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Accept": "application/json",
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.status == 204) {
            if (response.headers.get("action") == "follow") {
                document.querySelector("#follower-count").innerHTML = parseInt(document.querySelector("#follower-count").innerHTML) + 1;
                document.querySelector("#follow-button").innerHTML = "Unfollow"
            }
            else if (response.headers.get("action") == "unfollow") {
                document.querySelector("#follower-count").innerHTML = parseInt(document.querySelector("#follower-count").innerHTML) - 1;
                document.querySelector("#follow-button").innerHTML = "Follow"
            }
        }
    })
})