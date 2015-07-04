module.exports = function (app, passport, httpreq) {
    var Device = require('../app/models/device');
    var User = require('../app/models/user');
    var parser = "http://140.112.42.140:8888/";
	var rpi = "http://140.112.42.154:5566";
    // normal routes ===============================================================
    
    // show the home page (will also have our login links)
    app.get('/', function (req, res) {
        res.render('index.ejs');
    });
    
    // PROFILE SECTION =========================
    app.get('/profile', isLoggedIn, function (req, res) {
        Device.find({}, function (err, devices) {
            res.render('profile.ejs', {
                user : req.user,
                devices_list : devices
            });

        });
    });
    
    // Edit ===============
    
    app.get('/edit', isAdmin, function (req, res) {
        Device.find({}, function (err, devices) {
            User.find({}, function (err, user) {
                res.render('edit.ejs', {
                    user : user,
                    devices_list : devices
                });
            });
        });
    });
    
    
    
    // LOGOUT ==============================
    app.get('/logout', function (req, res) {
        req.logout();
        res.redirect('/');
    });
    
    // =============================================================================
    // AUTHENTICATE (FIRST LOGIN) ==================================================
    // =============================================================================
    
    // locally --------------------------------
    // LOGIN ===============================
    // show the login form
    app.get('/login', function (req, res) {
        res.render('login.ejs', { message: req.flash('loginMessage') });
    });
    
    // process the login form
    app.post('/login', passport.authenticate('local-login', {
        successRedirect : '/profile', // redirect to the secure profile section
        failureRedirect : '/login', // redirect back to the signup page if there is an error
        failureFlash : true // allow flash messages
    }));
    
    app.post('/mobelogin', function (req, res, next) {
        passport.authenticate('local-login', function (err, user, info) {
            if (err) {
                return next(err);
            }
            if (!user) {
                return res.send({ "msg": "login unsuccessful" });
            }
            req.login(user, function (err) {
                if (err) {
                    return next(err);
                }
                return res.send({ "msg": "login successful" });
            });
        })(req, res, next);
    });
    // SIGNUP =================================
    // show the signup form
    app.get('/signup', function (req, res) {
        res.render('signup.ejs', { message: req.flash('signupMessage') });
    });
    
    // process the signup form
    app.post('/signup', passport.authenticate('local-signup', {
        successRedirect : '/profile', // redirect to the secure profile section
        failureRedirect : '/signup', // redirect back to the signup page if there is an error
        failureFlash : true // allow flash messages
    }));
    
    app.post('/mobevoice', isLoggedIn, function (req, res) {
        httpreq.post(parser, { body: req.body.speechresult }, function (err, http_res, body) {
            console.log(body);
            var feedback = JSON.parse(body);
            if (feedback.success == true) {
                if (feedback.device_name == 'all') {
                    for (var i =0 ;i<req.user.local.allow_devices.length;i++) {
                        feedback.device_name = req.user.local.allow_devices[i];
                        httpreq.post(rpi, { body: JSON.stringify(feedback) }, function (err, http_res, body) {
                        });
                    }
                    res.send({ "msg": "Successful" });
                }
                else if (req.user.local.allow_devices.indexOf(feedback.device_name) != -1) {
                    //send http request
                    httpreq.post(rpi, { body: JSON.stringify(feedback) }, function (err, http_res, body) {
                        res.send({ "msg": "Successful" });
                    });
                }
                else {
                    res.send({ "msg": "Permission denied" });
                }
            }
            else {
                res.send({ "msg": "Unaccept command" });
            }
        });
    });
    
    app.post('/edit', function (req, res) {
        User.find({}, function (err, user) {
            for (var i in user) {
                if (user[i].local.permission != "admin") {
                    User.findOne({ 'local.name': user[i].local.name }, function (err, update_user) {
                        update_user.local.allow_devices = req.body[update_user.local.name];
                        update_user.save();
                    });
                }
            }
            res.redirect("/profile");
        });
    });
    app.get('/delete/:delete_user', isAdmin, function (req, res) {
        User.findOne({ 'local.name': req.params.delete_user }, function (err, d_user) {
            d_user.remove();
            res.redirect("/edit"); 
        })
    })
};

// route middleware to ensure user is logged in
function isLoggedIn(req, res, next) {
    if (req.isAuthenticated())
        return next();
    
    res.redirect('/');
}
function isAdmin(req, res, next) {
    if (req.isAuthenticated()) {
        if (req.user.local.permission == "admin")
            return next();
    }
    res.redirect('/');
}
