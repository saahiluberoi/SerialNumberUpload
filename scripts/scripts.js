<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
<script type=text/javascript>
        $(function() {
          $('a#test').on('click', function(e) {
            e.preventDefault()
            $.getJSON('process_file/',
                function(data) {
              //do nothing
            });
            return false;
          });
        });
</script>