$(function(){
  $.get('/graph', function(result) {
    /*var style = [
      { selector: 'node[label = "Person"]', css: {'background-color': '#6FB1FC','content': 'data(name)'}},
      { selector: 'node[label = "Movie"]', css: {'background-color': '#F5A45D','content': 'data(title)'}},
	   { selector: 'edge', css: {'curve-style': 'bezier','target-arrow-shape': 'triangle', 'content': 'data(relationship)'}} 
    ];*/

	//将cytoscape样式定义为变量cy
    var cy  = cytoscape({
      container: document.getElementById('cy'),	  // 定义需要渲染的容器
      /*style: style,*/
	  style:cytoscape.stylesheet()
      .selector('node').css({
			  'content': 'data(name)',
			  'font-size':24,
			  'background-image': 'data(img)',
			  'height': 100,
			  'width': 100,
			  'background-fit': 'cover',
			  'border-color': '#000',
			  'border-width': 3,
			  'border-opacity': 0.5}) //节点样式
     // .selector('node[性别 = "女"]').css({'background-color': '#F5A45D','content': 'data(name)','font-size':14})
		//.selector('node[label = "End"]').css({'background-color': '#666666','content': 'data(event)'})
	  .selector('edge').css({
			   'content': 'data(relationship)',
			   'curve-style': 'unbundled-bezier',
			   'width': 2,
			   'target-arrow-shape': 'triangle',
			   'line-color': '#ffaaaa',
			   'font-size':18,
			   'target-arrow-color': '#ffaaaa'
	  }) //边线样式
      .selector(':selected').css({'background-color': 'black','target-arrow-color': 'black','source-arrow-color': 'black','opacity': 0.7}) //点击后节点与边的样式
      .selector('.faded').css({'opacity': 0.25,'text-opacity': 0}),
      layout: { name:'breadthfirst',padding: 50},  //画布自适应大小
      elements: result.elements
	});



	  

    /* cy.nodes().forEach(function(ele) {
		ele.qtip({
			content: {
			text: function(ele){return 'Example qTip on ele ' + ele.data('id')},
			title: ele.data('name')
			},
			style: {
			classes: 'qtip-bootstrap'
			},
			position: {
			my: 'bottom center',
			at: 'top center',
			}
				
		})
	}); */
    cy.zoomingEnabled( false );

		
	cy.nodes().qtip({ //点击nodes处的提醒

		content:{ //function(){ return 'Example qTip on ele ' + this.id() },
			text: function(){
				//data = this._private.data;
				data = this.data()
				html = ""
				for (i = 0; i < Object.values(data).length; i++) {
					if (Object.keys(data)[i]=='img'){
						continue;
					}
					if (Object.keys(data)[i]=='id'){
						continue;
					}
					if (Object.keys(data)[i]=='label'){
						continue;
					}
					if (Object.keys(data)[i]=='name'){
						continue;
					}
    				html += Object.keys(data)[i]+"  :  "+Object.values(data)[i] + "<br>";
 				}
				return html;
			},

			title: function(){
				data = this._private.data;
				html = data['event'];
				return html
			}
		},
		position: {
			my: 'top center',
			at: 'bottom center'
		},
		style: {
			classes: 'qtip-bootstrap',
			tip: {
				width: 16,
				height: 8
			}
		}
	});

	cy.edges().qtip({
		content: {
			text: function(){
				//data = this._private.data;
				data = this.data()
				html = data.desc

				return html;
			}},
		position: {
			my: 'top center',
			at: 'bottom center'
		},
		show: {
			cyBgOnly: true
		},
		style: {
			classes: 'qtip-bootstrap',
			tip: {
				width: 16,
				height: 8
			}
		}
	});


			// call on core,点击空白处的提醒
	cy.qtip({
		content: '千与千寻人物关系图',
		position: {
			my: 'top center',
			at: 'bottom center'
		},
		show: {
			cyBgOnly: true
		},
		style: {
			classes: 'qtip-bootstrap',
			tip: {
				width: 16,
				height: 8
			}
		}
	});

    
	  /* cy.nodes().forEach(function(ele) {
			ele.qtip({
			  content: {
				text: qtipText(ele),
				title: ele.data('name')
			  },
			  style: {
				classes: 'qtip-bootstrap'
			  },
			  position: {
				my: 'bottom center',
				at: 'top center',
				target: ele
			  }
			})
		  });
    	
		function qtipText(node) {
		  
		  
		  var description = '<i>' + node.data('id') + '</i>';

		  return description + '</p>';
		} */
}, 'json');
});