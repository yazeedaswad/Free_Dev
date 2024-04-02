
//these two functions are used to validate during registartion if the given email already exits
// in the dabase such that there won't be duplicates

console.log("Hi")
const checkIfFreelancerExists = (e) => {

   
    const emailFormElement = e.target
    const email = e.target.value
    axios.post('/validate-freelancer-registration', {

        email: email
    })
    .then((response) => {

        if(response.data.user_exists == "true") {

            emailFormElement.setCustomValidity("The freelancer already exists. Please login instead")
            emailFormElement.reportValidity()
        }


    }, (error) => {

        console.log(error)


    })

    

}





const checkIfEmployerExists = (e) => {

   
    const emailFormElement = e.target
    const email = e.target.value
    axios.post('/validate-employer-registration', {

        email: email
    })
    .then((response) => {

        if(response.data.user_exists == "true") {

            emailFormElement.setCustomValidity("The employer already exists. Please login instead")
            emailFormElement.reportValidity()
        }


    }, (error) => {

        console.log(error)


    })

    

}