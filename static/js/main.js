
(function($) {

        "use strict";
    

    $(document).on('change', '#videoFile', function(event){
        
        console.log('in4');
        
        $('#alertError').html('')
        $('#checkFormat').prop('disabled', false)
        
        var file = document.getElementById('videoFile');
        var fileSize = Math.round((file.files[0].size / 1024))
        var fileName = file.files[0].name

        if (fileSize <= 5120){
            console.log('in2')
        }else if(fileSize > 5120){
            $('#alertError').html('Error File Size Too Large')
            $('#checkFormat').prop('disabled', true)
            console.log('in3')
        }
        

    
    })
       
    $(document).on('click', '#checkFformat', function(event){
        
        console.log('in');
        var file = document.getElementById('videoFile');
        var fileSize = Math.round((file.files[0].size / 1024))
        var fileName = file.files[0].name
        var fileData = new FormData()
        fileData.append('file', file.files[0])
        console.log(file.files[0])

        $.ajax(
            {
                url:"/objectSearch",
                method:"post",
                data:fileData,
                success:function(data)
                {
                    console.log(data);
                },
                });

    
    })

})(jQuery); // End of use strict