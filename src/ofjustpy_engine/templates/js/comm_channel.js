// Setup and manage communication between client and server
// event communication via websockes
// Assumes server side rendering.

    
var socket = null;
var msg = null;
var websocket_id = '';
var websocket_ready = false;
var web_socket_closed = false;
class JustpyCore {

	/**
	 * create a JustpyCore instance
	 * @param window
	 * @param {number} page_id - id of the page
	 * @param title - title of the document
	 * @param {boolean} use_websockets - If true use web sockets for communication otherwise ajax is used
	 * @param redirect
	 * @param display_url
	 * @param page_ready
	 * @param result_ready
	 * @param reload_interval_ms
	 * @param {string[]} events - event types the page should listen to
	 * @param {string} staticResourcesUrl - Url to static resources
	 * @param {boolean} debug - If true show debug messages
	 */
	constructor(window,
		page_id,
		title,
		use_websockets,
		redirect,
		display_url,
		page_ready,
		result_ready,
		reload_interval_ms,
		events,
		staticResourcesUrl,
		debug) {
		this.window = window;
		this.page_id = page_id;
		this.setTitle(title);
		this.use_websockets = use_websockets;
		if (redirect) {
			location.href = redirect;
		}
		if (display_url) {
			window.history.pushState("", "", display_url);
		}
		this.page_ready = page_ready;
		this.result_ready = result_ready;
		this.reload_interval_ms = reload_interval_ms;
		this.events = events;
		this.staticResourcesUrl = staticResourcesUrl;
		this.debug = debug;
	}

	/**
	 * set the title
	 * @param title - title of the document
	 */
	setTitle(title) {
		document.title = title;
		this.title = title;
	}

	/**
	 * setup the core functionality
	 */
	setup() {
		if (this.use_websockets) {
			this.setupWebSocket();
		} else {
			this.setupNoWebSocket();
		}
		this.registerAllEvents();
	}

	/**
	 * prepare WebSocket handling
	 */
	setupWebSocket() {
		console.log(location.protocol + ' Domain: ' + document.domain);
		if (location.protocol === 'https:') {
			var protocol_string = 'wss://'
		} else {
			protocol_string = 'ws://'
		}
		var ws_url = protocol_string + document.domain;
		if (location.port) {
			ws_url += ':' + location.port;
		}
		socket = new WebSocket(ws_url);

		socket.addEventListener('open', function(event) {
			console.log('Websocket opened');
			socket.send(JSON.stringify({ 'type': 'connect', 'page_id': page_id }));
		});

		// on error reload site
		socket.addEventListener('error', function(event) {
			reload_site();
		});

		// if side closed → close websocket
		socket.addEventListener('close', function(event) {
			console.log('Websocket closed');
			web_socket_closed = true;
			reload_site()
		});

	    socket.addEventListener('message', function(event) {
		console.log('message Event listen', event);
			this.handleMessageEvent(event);
		}.bind(this));  // handover the class context to the event listener function
	}

	/**
	 * Handles the message event
	 * https://developer.mozilla.org/en-US/docs/Web/API/MessageEvent
	 * @param event
	 */
    handleMessageEvent(event) {

	msg = JSON.parse(event.data);
	
		// if (this.debug) {

		//}
		switch (msg.type) {
			case 'page_update':
				this.handlePageUpdateEvent(msg);
				break;

			case 'websocket_update':
				this.handleWebsocketUpdateEvent(msg);
				break;

			case 'run_javascript':
				this.handleRunJavascriptEvent(msg);
				break;
                       case 'diff_patch_update':
				this.handleDiffPatchUpdate(msg);
				break;
			case 'update_cookies':
				this.update_cookies(msg);
				break;
		       case 'run_method':
				// await websocket.send_json({'type': 'run_method', 'data': command, 'id': self.id})
				eval('comp_dict[' + msg.id + '].' + msg.data);
				break;

			case 'chart_update':
				const chart = cached_graph_def['chart' + msg.id];
				chart.update(msg.data);
				break;
			case 'tooltip_update':
				this.handleTooltipUpdate(msg);
				break;
			default: {
				if (this.debug) {
					console.log("Message type " + msg.type + " has no registered event handler");
				}
			}
		}
	}

	/**
	 * handles the page_update event
	 */
	handlePageUpdateEvent(msg) {
		if (msg.page_options.redirect) {
			location.href = msg.page_options.redirect;
			return;
		}
		if (msg.page_options.open) {
			window.open(msg.page_options.open, '_blank');
		}
		if (msg.page_options.display_url !== null)
			window.history.pushState("", "", msg.page_options.display_url);
		document.title = msg.page_options.title;
		if (msg.page_options.favicon) {
			var link = document.querySelector("link[rel*='icon']") || document.createElement('link');
			link.type = 'image/x-icon';
			link.rel = 'shortcut icon';
			if (msg.page_options.favicon.startsWith('http')) {
				link.href = msg.page_options.favicon;
			} else {
				link.href = this.staticResourcesUrl + msg.page_options.favicon;
			}
			document.getElementsByTagName('head')[0].appendChild(link);
		}
	}

	/**
	 * Handles the websocket_update event
	 * @param msg
	 */

    update_cookies(msg){
    let cookie_json_data = msg.data;
	for (const stateAttrName in cookie_json_data) {
	const cookieData = cookie_json_data[stateAttrName];	
		const cookieName = cookieData.cookie_name;
		const cookieTTL = cookieData.cookie_ttl;
		const cookieProperties = cookieData.cookie_properties;
		const signedData = cookieData.signed_data; 
		const expirationDate = new Date();
		expirationDate.setTime(expirationDate.getTime() + cookieTTL * 1000);
		const cookieString = `${cookieName}=${encodeURIComponent(signedData)}; ` +
			`expires=${expirationDate.toUTCString()}; ` +
			`path=${cookieProperties.path}` +
			(cookieProperties.domain ? `; domain=${cookieProperties.domain}` : '') +
			(cookieProperties.secure ? '; secure' : '') +
			(cookieProperties.httponly ? '; HttpOnly' : '') +
			`; samesite=${cookieProperties.samesite}`;

		document.cookie = cookieString;
		
	}

    }
    handleDiffPatchUpdate(msg){
	let data = msg.data
	for (var id in data) {
	    var element = document.getElementById(id);
	    if (element){
		if (element.tagName == "CANVAS"){
		    //proxy to indicate a chart update
		    //if there are other items other then Chart
		    //in CANVAS we need to update that
		    const chartContext = element.getContext('2d');
		    const chartInstance = jpComponentBuilder.ChartJSChart.getChart(chartContext);
		    if (data[id].hasOwnProperty('domDict')) {
			var domDict = data[id].domDict;
			for (let [key, value] of Object.entries(domDict)) {
				updateChartConfig(chartInstance, key, value);
			}
		    }
		    //const chartOptions = chartInstance.options;
		    //chartOptions.scales.x.title.text = "newtitle"
		    //chartInstance.update()
		    //const config = chartInstance.config;
		    //config.scales.x.title.text = "abctitlee";
		}
		if (data[id].hasOwnProperty('domDict')) {
		    var domDict = data[id].domDict;
		    if (domDict.hasOwnProperty('/classes')) {
			element.className = domDict['/classes'];
		    }
		    if (domDict.hasOwnProperty('/text')) {
			element.innerText = domDict['/text'];
		    }
		}
		if (data[id].hasOwnProperty('attrs')) {
		    var attrs = data[id].attrs;
		    for (var attr in attrs){
			if (attr === "/disabled"){
			    if (attrs[attr] === "False"){
				element.removeAttribute("disabled");
			    }
			    if (attrs[attr] === "True"){
				    element.setAttribute("disabled", "");
			    }
			}
		    }
		}
	    }
	}
    }
	handleWebsocketUpdateEvent(msg) {
		websocket_id = msg.data;
		websocket_ready = true;
		if (this.page_ready) {
			const e = {
				'event_type': 'page_ready',
				'visibility': document.visibilityState,
				'page_id': page_id,
				'websocket_id': websocket_id
			};
			send_to_server(e, 'page_event', false);
		}
	}

	/**
	* handle Error
	*/
	handleError(error) {
		if (this.debug) {
			console.log(error);
		}
		this.send_result("Error in javascript")
	}

	/**
	 * send javascript eval result back to server
	 * @param js_result - the javascript result to send
	 */
	send_result(js_result) {
		let e = {
			'event_type': 'result_ready',
			'visibility': document.visibilityState,
			'page_id': this.page_id,
			'websocket_id': websocket_id,
			'request_id': msg.request_id,
			'result': js_result //JSON.stringify(js_result)
		};
		if (this.result_ready) {
			if (msg.send) {
				send_to_server(e, 'page_event', false);
			}
		}
	}

	/**
	 * Handles the run_javascript event
	 * @param msg
	 */
	handleRunJavascriptEvent(msg) {
		/**
		 * callback to send javascript result back to server
		 */
		const jsPromise = new Promise((resolve, reject) => {
			try {
				let eval_result = eval(msg.data)
				resolve(eval_result)
			} catch (error) {
				reject(error)
			}
		});
		jsPromise.then((value) => {
			this.send_result(value);
		}).catch((error) => {
			this.handleError(error);
		});
	}

	/**
	 * setup page without websockets
	 * https://developer.mozilla.org/en-US/docs/Web/API/Window/beforeunload_event
	 */
	setupNoWebSocket() {
		window.addEventListener('beforeunload', function(event) {
			let e = {
				'event_type': 'beforeunload',
				'page_id': page_id,
			};
			send_to_server(e);
		});
	}

	/**
	 * setup the reload interval
	 */
	setupReloadInterval() {
		if (this.reload_interval_ms > 0) {
			setInterval(function() {
				$.ajax({
					type: "POST",
					url: "/zzz_justpy_ajax",
					data: JSON.stringify({
						'type': 'event',
						'event_data': { 'event_type': 'page_update', 'page_id': this.page_id }
					}),
					success: function(msg) {
					    if (msg) {
						jpComponentBuilder.justpyComponents.set(msg.data)
						//app1.$set({justpyComponents : msg.data});
					    }
					},
					dataType: 'json'
				});
			}, this.reload_interval_ms);
		}
	}

	/**
	 * register all events
	 */
	registerAllEvents() {
		for (const event of this.events) {
			this.registerEventListener(event);
		}
	}

	/**
	 * adds an event listener to the given event that sends the event with key data to the server
	 * @param {string} event - event type to add the event listener to
	 */
	registerEventListener(event) {
		document.addEventListener(event, function(evt) {
			const e = {
				'event_type': event,
				'visibility': document.visibilityState,
				'page_id': page_id,
				'websocket_id': websocket_id
			};
			if (evt instanceof KeyboardEvent) {
				// https://developer.mozilla.org/en-US/docs/Web/Events/keydown   keyup, keypress
				e['key_data'] = {
					altKey: evt.altKey,
					ctrlKey: evt.ctrlKey,
					shiftKey: evt.shiftKey,
					metaKey: evt.metaKey,
					code: evt.code,
					key: evt.key,
					location: evt.location,
					repeat: evt.repeat,
					locale: evt.locale
				}
			}
			send_to_server(e, 'page_event', false);
		});
	}
}
