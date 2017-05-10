/* exported Script */
/* globals console, _, s */

/** Global Helpers
 *
 * console - A normal console instance
 * _       - An underscore instance
 * s       - An underscore string instance
 */

//function blatantly stolen
function dateDiff(datepart, fromdate, todate) {	
  datepart = datepart.toLowerCase();	
  var diff = todate - fromdate;	
  var divideBy = { w:604800000, 
                   d:86400000, 
                   h:3600000, 
                   n:60000, 
                   s:1000 };	
  
  return Math.floor( diff/divideBy[datepart]);
}

//function blatantly stolen and modified
function getFormattedDate(d, offset){
    // convert to msec
    // add local time zone offset
    // get UTC time in msec
    var utc = d.getTime() + (d.getTimezoneOffset() * 60000);

    // create new Date object for different city
    // using supplied offset
    var nd = new Date(utc + (3600000*offset));


	dstr = d.getFullYear() + "-" + ('0' + (d.getMonth() + 1)).slice(-2) + "-" + ('0' + d.getDate()).slice(-2) + " " + nd.toLocaleTimeString();
	//d = d.toLocaleString();  
    return dstr;
}





class Script {
  /**
   * @params {object} request
   */
  process_incoming_request({ request }) {


    //console is a global helper to improve debug
	// console.log(request.content);
    
    var myContent = request.content; 
     
    if (myContent.start.dateTime) {
		var dateStart  	= new Date(myContent.start.dateTime);
	} else {
		var dateStart  	= new Date(myContent.start.date);	
	}
	var dateStartText 	= getFormattedDate(dateStart,2);
	
    if (myContent.end.dateTime) {
		var dateEnd  	= new Date(myContent.end.dateTime);
	} else {
		var dateEnd  	= new Date(myContent.end.date);	
	}
	var dateEndtText 	= getFormattedDate(dateEnd,2);

	var duration = 	dateDiff('n', dateStart, dateEnd);
	var durationText;
	if (duration < 300) {
		durationText = duration + ' minutes ';
	} else {
		duration = 	dateDiff('h', dateStart, dateEnd);
		durationText = duration + ' hours ';	
		if (duration > 24) {
			duration = 	dateDiff('d', dateStart, dateEnd);
			durationText = durationText + ' ( ' + duration + ' days )';	
		}	
	}

            
    var myText = myContent.organizer.displayName + " Calendar Event \n";
    myText = myText + 'Summary:  *' + myContent.summary + '*\n';
    myText = myText + 'Start:    *' + dateStartText +'*\n';    	
	myText = myText + 'End:    *' + dateEndtText +'*\n';     
    myText = myText + 'Duration:      *' + durationText + ' * \n';
    myText = myText + 'Link:	 ' + myContent.htmlLink + '\n';
    if (myContent.description) {
    	myText = myText + 'Description:      *' + myContent.description + '*\n';
    }
    if (myContent.hangoutLink) {
    	myText = myText + 'Hangout:      ' + myContent.hangoutLink + '\n';    	
    }
    if (myContent.location) {
    	myText = myText + 'Location:      *' + myContent.location + '*\n';    	
    }
    
    return {
      content:{
        text: myText
       }
    };

  }
}