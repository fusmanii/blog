<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Blog - Post</title>

    <!-- Bootstrap Core CSS -->
     <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">

    <!-- Theme CSS -->
    <link href="{{ get_url('static', filename='css/clean-blog.css') }}" rel="stylesheet">

    <!-- Custom Fonts -->
    <link href="{{ get_url('static', filename='vendor/font-awesome/css/font-awesome.min.css') }}" rel="stylesheet" type="text/css">
    <link href='http://fonts.googleapis.com/css?family=Lora:400,700,400italic,700italic' rel='stylesheet' type='text/css'>
    <link href='http://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800' rel='stylesheet' type='text/css'>

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->

</head>

<body onload="loadScroll()" onunload="saveScroll()">

    <!-- Navigation -->
    <nav class="navbar navbar-default navbar-custom navbar-fixed-top">
        <div class="container-fluid">
            <!-- Brand and toggle get grouped for better mobile display -->
            <div class="navbar-header page-scroll">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
                    <span class="sr-only">Toggle navigation</span>
                    Menu <i class="fa fa-bars"></i>
                </button>
                % if username:
                <a class="navbar-brand" href="/">Welcome {{ username }}</a>
                % else:
                <a class="navbar-brand" href="/">Simple Blog</a>
                % end
            </div>

            <!-- Collect the nav links, forms, and other content for toggling -->
            <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                <ul class="nav navbar-nav navbar-right">
                    % if username:
                    <li>
                        <a href="/">Home</a>
                    </li>
                    <li>
                        <a href="/newpost">New Post</a>
                    </li>
                    <li>
                        <a href="/logout">Log Out</a>
                    </li>
                    % else:
                    <li>
                        <a href="/">Home</a>
                    </li>
                    <li>
                        <a href="/signup">Sign Up</a>
                    </li>
                    <li>
                        <a href="/login">Login</a>
                    </li>
                    % end
                </ul>
            </div>
            <!-- /.navbar-collapse -->
        </div>
        <!-- /.container -->
    </nav>

    <!-- Page Header -->
    <!-- Set your background image for this header on the line below. -->
    <header class="intro-header" style="background-image: url(/image/{{post['permalink']}})">

        <div class="container">
            <div class="row">
                <div class="col-lg-8 col-lg-offset-2 col-md-10 col-md-offset-1">
                    <div class="post-heading">
                        <h1>{{ !post['title'] }}</h1>
                        <span class="meta">Posted by <a href="#">{{ post['author'] }}</a> on {{ post['date'] }}</span>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <!-- Post Content -->
    <article>
        <div class="container">
            <div class="row">
                <div class="col-lg-8 col-lg-offset-2 col-md-10 col-md-offset-1">
                    {{ post['body'] }}
                    <hr>

                    <div class="row">
                        <h4>Comments {{len(post.get('comments', []))}}<h4>
                    </div>
                    %for i in range(len(post.get('comments', []))):
                    <div class="post-preview">
                        <h2 class="post-title">
                            {{ post['comments'][i]['author'] }}
                        </h2>
                        <form action="/like" method="POST">
                            <input type="hidden" name="permalink", value="{{post['permalink']}}">
                            <input type="hidden" name="commentOrdinal", value="{{i}}">
                                Likes: {{post['comments'][i]['numLikes']}} 
                            <input type="submit" class="btn btn-primary btn-sm" value="Like">
                        </form><br>
                        <p class="post-subtitle">
                            {{ post['comments'][i]['body'] }}
                        </p>
                    </div>
                    <hr>
                    %end

        			<!-- Contact Section -->
                    <section id="contact">
                        <div class="">
                            <div class="row">
                                <div>
                                    <h3>Add a comment</h3>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-lg-8">
                                    <!-- To configure the contact form email address, go to mail/contact_me.php and update the email address in the PHP file on line 19. -->
                                    <!-- The form should work on most web servers, but if the form is not working you may need to configure your web server differently. -->
                                    <form action="/newcomment" method="POST" novalidate>
                                    <input type="hidden" id="permalink" name="permalink", value="{{post['permalink']}}">
                                        <div class="row control-group">
                                            <div class="form-group col-xs-12 floating-label-form-group controls">
                                                <label>Name</label>
                                                <input type="text" class="form-control" placeholder="Name" id="name" required data-validation-required-message="Please enter your name." name="name">
                                                <p class="help-block text-danger"></p>
                                            </div>
                                        </div>
                                        <div class="row control-group">
                                            <div class="form-group col-xs-12 floating-label-form-group controls">
                                                <label>Email Address</label>
                                                <input type="email" class="form-control" placeholder="Email Address" id="email" required data-validation-required-message="Please enter your email address." name="email">
                                                <p class="help-block text-danger"></p>
                                            </div>
                                        </div>
                                        <div class="row control-group">
                                            <div class="form-group col-xs-12 floating-label-form-group controls">
                                                <label>Message</label>
                                                <textarea rows="5" class="form-control" placeholder="Message" id="message" required data-validation-required-message="Please enter a message." name="message"></textarea>
                                                <p class="help-block text-danger"></p>
                                            </div>
                                        </div>
                                        <input type="hidden" name="permalink", value="{{post['permalink']}}">
                                        <br>
                                        <div id="success"></div>
                                        <div class="row">
                                            <div class="form-group col-xs-12">
                                                <button type="submit" class="btn btn-success btn-lg">Submit</button>
                                            </div>
                                        </div>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </section> 
                </div>
            </div>
        </div>
    </article>

    <hr>

    <!-- Footer -->
    <footer>
        <div class="container">
            <div class="row">
                <div class="col-lg-8 col-lg-offset-2 col-md-10 col-md-offset-1">
                    <ul class="list-inline text-center">
                        <li>
                            <a href="https://www.linkedin.com/in/fusmanii/">
                                <span class="fa-stack fa-lg">
                                    <i class="fa fa-circle fa-stack-2x"></i>
                                    <i class="fa fa-linkedin fa-stack-1x fa-inverse"></i>
                                </span>
                            </a>
                        </li>
                        <li>
                            <a href="https://www.facebook.com/fusmanii">
                                <span class="fa-stack fa-lg">
                                    <i class="fa fa-circle fa-stack-2x"></i>
                                    <i class="fa fa-facebook fa-stack-1x fa-inverse"></i>
                                </span>
                            </a>
                        </li>
                        <li>
                            <a href="https://github.com/fusmanii">
                                <span class="fa-stack fa-lg">
                                    <i class="fa fa-circle fa-stack-2x"></i>
                                    <i class="fa fa-github fa-stack-1x fa-inverse"></i>
                                </span>
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </footer>

    <script type="text/javascript">
    function saveScroll() {
        var expdate = new Date();
        expdate.setTime(expdate.getTime() + (expdays*24*60*60*1000)); // expiry date

        var x = document.pageXOffset || document.body.scrollLeft;
        var y = document.pageYOffset || document.body.scrollTop;
        var data = x + "_" + y;
        setCookie(cookieName, data, expdate);
    }

    function loadScroll() {
        var inf = getCookie(cookieName);
        if (!inf) { return; }
        var ar = inf.split("_");
        if (ar.length == 2) {
            window.scrollTo(parseInt(ar[0]), parseInt(ar[1]));
        }
    }
    </script>

    <!-- jQuery -->
    <script src="{{ get_url('static', filename='vendor/jquery/jquery.min.js') }}"></script>

    <!-- Bootstrap Core JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>

    <!-- Contact Form JavaScript -->
    <script src="{{ get_url('static', filename='js/jqBootstrapValidation.js') }}"></script>
    <script src="{{ get_url('static', filename='js/contact_me.js') }}"></script>

    <!-- Theme JavaScript -->
    <script src="{{ get_url('static', filename='js/clean-blog.min.js') }}"></script>

</body>

</html>
