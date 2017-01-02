// not used anymore
var DEFAULT_HASH = 'home';

//setup crossroads
crossroads.addRoute('home', function() {
    alert('Home');
});
crossroads.addRoute('lorem', function(){
    alert('lorem');
});
crossroads.addRoute('lorem/ipsum', function(){
    alert('lorem/ipsum');
});
crossroads.routed.add(console.log, console); //log all routes

//setup hasher


function parseHash(newHash, oldHash){
    // second parameter of crossroads.parse() is the "defaultArguments" and should be an array
    // so we ignore the "oldHash" argument to avoid issues.
    crossroads.parse(newHash);
}
hasher.initialized.add(parseHash); //parse initial hash
hasher.changed.add(parseHash); //parse hash changes

hasher.init(); //start listening for hash

//only required if you want to set a default value
if(! hasher.getHash()){
    hasher.setHash(DEFAULT_HASH);
}