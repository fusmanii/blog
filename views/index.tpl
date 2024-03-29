<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Clean Blog</title>

    <!-- Bootstrap Core CSS -->
    <link href="{{ get_url('static', filename='vendor/bootstrap/css/bootstrap.min.css')}}" rel="stylesheet">

    <!-- Theme CSS -->
    <link href="{{ get_url('static', filename='css/clean-blog.min.css')}}" rel="stylesheet">

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

<body>

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
    <header class="intro-header" style="background-image: url({{ get_url('static', filename='img/intro.jpg') }})">
        <div class="container">
            <div class="row">
                <div class="col-lg-8 col-lg-offset-2 col-md-10 col-md-offset-1">
                    <div class="site-heading">
                        <h1>Blog</h1>
                        <hr class="small">
                        <span class="subheading">A Blog</span>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <div class="container">
        <div class="row">
            <div class="col-lg-8 col-lg-offset-2 col-md-10 col-md-offset-1">

                %for post in posts:
                <div class="post-preview">
                    <a href="/post/{{post['permalink']}}">
                        <img src="/thumb/{{post['permalink']}}" alt="Smiley face" height="60" width="80">
                        <h2 class="post-title">
                            {{post['title']}}
                        </h2>
                        <h3 class="post-subtitle">
                            {{post['body'].split('.')[0] + '...'}}
                        </h3>
                    </a>
                    <p class="post-meta">Posted by <a href="#">{{post['author']}}</a> on {{post['date']}}</p>
                    %if ('tags' in post):
                    %for t in post['tags'][0:1]:
                    <p class="post-meta"> <a href="/tag/{{t}}">{{t}}</a>
                    %end
                    %for t in post['tags'][1:]:
                    , <a href="/tag/{{t}}">{{t}}</a>
                    %end
                    </p>
                    %end
                </div>
                <hr>
                %end

                <!-- Pager -->
                <ul class="pager">
                    % if page > 1:
                    <li class="previous">
                        <a href="{{(('/tag/' + tag) if tag else '') + '/' + str(prevPage)}}">&larr; Newer Posts</a>
                    </li>
                    % end
                    % if nextPage > 1:
                    <li class="next">
                        <a href="{{(('/tag/' + tag) if tag else '') + '/' + str(nextPage)}}">Older Posts &rarr;</a>
                    </li>
                    % end
                </ul>
            </div>
        </div>
    </div>

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

    <!-- jQuery -->
    <script src="{{ get_url('static', filename='vendor/jquery/jquery.min.js') }}"></script>

    <!-- Bootstrap Core JavaScript -->
    <script src="{{ get_url('static', filename='vendor/bootstrap/js/bootstrap.min.js') }}"></script>

    <!-- Contact Form JavaScript -->
    <script src="{{ get_url('static', filename='js/jqBootstrapValidation.js') }}"></script>
    <script src="{{ get_url('static', filename='js/contact_me.js') }}"></script>

    <!-- Theme JavaScript -->
    <script src="{{ get_url('static', filename='js/clean-blog.min.js') }}"></script>

</body>

</html>
