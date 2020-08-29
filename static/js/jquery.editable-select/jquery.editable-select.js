/**
 * Copyright (c) 2009 Anders Ekdahl (http://coffeescripter.com/)
 *  var select = $('.editable-select:first');
 *  var instances = select.editableSelectInstances();
 *  instances[0].addOption('Germany', 'value added programmatically');
 *
 * Version: 1.3.2
 * yingxian modify
 * Demo and documentation: http://coffeescripter.com/code/editable-select/
 */
(function($) {
  var instances = [];
  $.fn.editableSelect = function(options) {
    var defaults = { bg_iframe: false,
                     onSelect: false,
                     items_then_scroll: 10,
                     case_sensitive: false
    };
    var settings = $.extend(defaults, options);
    // Only do bg_iframe for browsers that need it
    /*if(settings.bg_iframe && !$.browser.msie) {
      settings.bg_iframe = false;
    };*/
    var instance = false;
    $(this).each(function() {
      var i = instances.length;
      if($(this).data('editable-selecter') !== null) {
        instances[i] = new EditableSelect(this, settings);
        $(this).data('editable-selecter', i);
      };
    });
    return $(this);
  };
  $.fn.editableSelectInstances = function() {
    var ret = [];
    $(this).each(function() {
      if($(this).data('editable-selecter') !== null) {
        ret[ret.length] = instances[$(this).data('editable-selecter')];
      };
    });
    return ret;
  };

  var EditableSelect = function(select, settings) {
    this.init(select, settings);
  };
  EditableSelect.prototype = {
    settings: false,
    text: false,
    select: false,
    select_width: 0,
    wrapper: false,
    list_item_height: 20,
    list_height: 0,
    list_is_visible: false,
    hide_on_blur_timeout: false,
    bg_iframe: false,
    current_value: '',
    init: function(select, settings) {
      this.settings = settings;
      this.wrapper = $(document.createElement('div'));
      this.wrapper.addClass('editable-select-options');
      this.select = $(select);
      var name = this.select.attr('name');
      if(!name) {
        name = 'editable-select'+ instances.length;
      };
      var id = this.select.attr('id');
      if(!id) {
        id = 'editable-select'+ instances.length;
      };
      this.text = $('<input type="text">');
      this.text_submit = $('<input type="hidden">');
      this.text.attr('name', name + "_sele");
      this.text_submit.attr('name', name);
      this.text.data('editable-selecter', this.select.data('editable-selecter'));
      this.text_submit.data('editable-selecter', this.select.data('editable-selecter'));
      // Because we don't want the value of the select when the form
      // is submitted
      this.select.attr('disabled', 'disabled');
      this.text[0].className = this.select[0].className;
      this.text_submit[0].className = this.select[0].className;
      
      this.text.attr('id', id + "_sele");
      this.text_submit.attr('id', id);
      this.wrapper.attr('id',id+'_editable-select-options');
      this.text.attr('autocomplete', 'off');
      this.text.attr('autocomplete', 'off');
      this.text.addClass('editable-select');
      this.text_submit.addClass('editable-select');
      this.select.attr('id', id +'_hidden_select');
      this.select.attr('name', name +'_hidden_select');
      this.select.after(this.text);
      this.select.after(this.text_submit);
      if(this.select.css('display') == 'none') {
        //this.text.css('display', 'none');
        this.text_submit.css('display', 'none');
      }
      if(this.select.css('visibility') == 'hidden') {
        //this.text.css('visibility', 'visibility');
        this.text_submit.css('visibility', 'visibility');
      }
      // Set to hidden, because we want to call .show()
      // on it to get it's width but not having it display
      // on the screen
      this.select.css('visibility', 'hidden');
      this.select.hide();
      this.initInputEvents(this.text);
      this.duplicateOptions();
      this.setWidths();
      $(document.body).append(this.wrapper);
 
      if(this.settings.bg_iframe) {
        this.createBackgroundIframe();
      };
      if(typeof this.settings.success == "function") {
    	  this.settings.success.call(this,this.text_submit[0]);
      };
    },
    /**
     * Take the select lists options and
     * populate an unordered list with them
     */
    duplicateOptions: function() {
      var context = this,text,val;
      var option_list = $(document.createElement('ul'));
      this.wrapper.empty();
      this.wrapper.append(option_list);
      var options = this.select.find('option');
      this.dataList = [];
      options.each(function(i) {
    	text = $(this).text();
    	val = $(this).val();
        if($(this).attr('selected') /*|| i == 0*/) {
          context.text.val(text);
          context.text_submit.val(val);
          context.current_value = text;
        };
        if(context.trim(text) != "") context.dataList.push(text);
        var li = $('<li value="'+ val +'">'+ text +'</li>');
        li.hide();
        context.initListItemEvents(li);
        option_list.append(li);
      });
      this.setWidths();
      this.checkScroll();
    },in_array:function(e,arr)
    {
    	for(i=0,len = arr.length;i < len;i++)
    	{
	    	if(arr[i] == e)
	    	{
	    	  return true;
	    	}
       }
       return false;
    },trim:function(str){
    	return typeof str == "string" ? str.replace(/^\s*|\s*$/g,"") : str;
    },
    /**
     * Check if the list has enough items to display a scroll
     */
    checkScroll: function() {
      var options = this.wrapper.find('li');
      if(options.length > this.settings.items_then_scroll) {
        this.list_height = this.list_item_height * this.settings.items_then_scroll;
        this.wrapper.css('height', this.list_height +'px');
        this.wrapper.css('overflow', 'auto');
      } else {
        this.wrapper.css('height', 'auto');
        this.wrapper.css('overflow', 'visible');
      };
    },
    addOption: function(value,text) {
      var li = $('<li value="' + value + '">'+ text +'</li>');
      var option = $('<option value="' + value + '">'+ text +'</option>');
      this.select.append(option);
      this.initListItemEvents(li);
      this.wrapper.find('ul').append(li);
      this.setWidths();
      this.checkScroll();
    },
    /**
     * Init the different events on the input element
     */
    initInputEvents: function(text) {
      var context = this;
      var timer = false;
      $(document.body).click(
        function() {
          context.clearSelectedListItem();
          context.hideList();
        }
      );
      text.blur(
	        function(e) {
	          var val = context.trim(this.value);
	          var isInArr = context.in_array(val,context.dataList);
	          if( val == "")
        	  {
	        	  context.text_submit.val("");
        	  }else if(val != "" && !isInArr)
        	  {
	        	  context.text_submit.val("-1");
        	  }

	          var list_item = typeof context.settings.onSelect == 'function' && isInArr ? context.findItem(val) : null;
		      
	          if(typeof context.settings.onSelect == 'function' && list_item != null) {
	
	        	  context.text.val(list_item.text());
	        	  context.text_submit.val(list_item.attr("value"));
	        	  context.current_value = context.text.val();
	              context.settings.onSelect.call(context, list_item,context.text_submit[0]);
	          };
	          
	          context.hideList();
	            
	          e.preventDefault();
	          e.stopPropagation();
	     }
      );
      text.focus(
        function(e) {
          // Can't use the blur event to hide the list, because the blur event
          // is fired in some browsers when you scroll the list
          context.showList();
          context.highlightSelected();
          e.stopPropagation();
        }
      ).click(
        function(e) {
          e.stopPropagation();
          context.showList();
          context.highlightSelected();
        }
      ).keydown(
        // Capture key events so the user can navigate through the list
        function(e) {
          switch(e.keyCode) {
            // Down
            case 40:
              if(!context.listIsVisible()) {
                context.showList();
                context.highlightSelected();
              } else {
                e.preventDefault();
                context.selectNewListItem('down');
              };
              break;
            // Up
            case 38:
              e.preventDefault();
              context.selectNewListItem('up');
              break;
            // Tab
            case 9:
              context.pickListItem(context.selectedListItem());
              break;
            // Esc
            case 27:
              e.preventDefault();
              context.hideList();
              return false;
              break;
            // Enter, prevent form submission
            case 13:
              e.preventDefault();
              context.pickListItem(context.selectedListItem());
              return false;
          };
        }
      ).keyup(
        function(e) {
          // Prevent lots of calls if it's a fast typer
          if(timer !== false) {
            clearTimeout(timer);
            timer = false;
          };
          timer = setTimeout(
            function() {
              // If the user types in a value, select it if it's in the list
              if(context.text.val() != context.current_value) {
                context.current_value = context.text.val();
                context.highlightSelected();
                //context.showList();
              };
            },
            200
          );
          
          // if input text change,list show.yingxian add hack by 2013-09-08
          (e.keyCode == 13) ?  context.hideList() : context.showList();
    	   e.stopPropagation();
        }
      ).keypress(
        function(e) {
          if(e.keyCode == 13) {
            // Enter, prevent form submission
            e.preventDefault();
            return false;
          };
        }
      );
    },
    initListItemEvents: function(list_item) {
      var context = this;
      list_item.mouseover(
        function() {
          context.clearSelectedListItem();
          context.selectListItem(list_item);
        }
      ).mousedown(
        // Needs to be mousedown and not click, since the inputs blur events
        // fires before the list items click event
        function(e) {
          e.stopPropagation();
          context.pickListItem(context.selectedListItem());
        }
      );
    },
    selectNewListItem: function(direction) {
      var li = this.selectedListItem();
      if(!li.length) {
        li = this.selectFirstListItem();
      };
      if(direction == 'down') {
        var sib = this.selectNextItem(li);
      } else {
        var sib = this.selectPrevItem(li);
      };
      if(sib.length) {
        this.selectListItem(sib);
        this.scrollToListItem(sib);
        this.unselectListItem(li);
      };
    },selectNextItem:function(el){
    	var e = el.next();
    	if(e && e[0].display == "none")
		{
    		return el;
		}
    	return e;
    },selectPrevItem:function(el){
    	
    	var e = el.prev();
    	if(e && e[0].display == "none")
		{
    		return el;
		}
    	return e;
    	
    },
    selectListItem: function(list_item) {
      this.clearSelectedListItem();
      list_item.addClass('selected');
    },
    selectFirstListItem: function() {
      this.clearSelectedListItem();
      var first = this.wrapper.find('li:first');
      //this.wrapper.find('li').hide();
      first.addClass('selected');
      //first.show();
      return first;
    },
    unselectListItem: function(list_item) {
      list_item.removeClass('selected');
    },
    selectedListItem: function() {
		alert(this.wrapper.find('li.selected').val());
      return this.wrapper.find('li.selected');
    },
    clearSelectedListItem: function() {
      this.wrapper.find('li.selected').removeClass('selected');
    },
    /**
     * The difference between this method and selectListItem
     * is that this method also changes the text field and
     * then hides the list
     */
    pickListItem: function(list_item) {
      if(list_item.length) {
        this.text.val(list_item.text());
        this.text_submit.val(list_item.attr("value"));
        this.current_value = this.text.val();
      };
      if(typeof this.settings.onSelect == 'function') {
        this.settings.onSelect.call(this, list_item,this.text_submit[0]);
      };
      this.hideList();
    },
    listIsVisible: function() {
      return this.list_is_visible;
    },
    showList: function() {
      this.positionElements();
      this.setWidths();
      this.wrapper.show();
      this.hideOtherLists();
      this.list_is_visible = true;
      if(this.settings.bg_iframe) {
        this.bg_iframe.show();
      };
    },
    findItem: function(text1) {
    	var context = this;
        var current_value = context.trim(text1);
    	var list_items = context.wrapper.find('li');
    	var best_candiate = false;
        var value_found = false;
    	list_items.each(
    	        function() {
    	        	var text = context.trim($(this).text());
    	            if(!value_found) {
    	              if(!context.settings.case_sensitive) {
    	                text = text.toLowerCase();
    	              };
    	              if(text == current_value) {
    	                value_found = true;
    	                best_candiate = $(this);
    	                return false;
    	              }
    	            };
    	
    	          }
    	      
    	   );
    	
    	  if(value_found) {
    		  return best_candiate;
          }else if(!best_candiate && !value_found) {
        	  return null;
          }; 
    	  
      },
    highlightSelected: function() {
      var context = this;
      var current_value = context.trim(this.text.val());
      if(current_value.length < 0) {
        if(highlight_first) {
          this.selectFirstListItem();
        };
        return;
      };
      
      var list_items = this.wrapper.find('li');
      if(current_value.length == 0) {
    	  list_items.show();
    	  this.selectFirstListItem();
          return;
       };
        
      if(!context.settings.case_sensitive) {
        current_value = current_value.toLowerCase();
      };
      var best_candiate = false;
      var value_found = false;
      list_items.each(
        function() {
          var text = $(this).text();
          if(!value_found) {
            if(!context.settings.case_sensitive) {
              text = text.toLowerCase();
            };
            if(text == current_value) {
              value_found = true;
              context.clearSelectedListItem();
              context.selectListItem($(this));
              context.scrollToListItem($(this));
              //return false;
            } else if(text.search(current_value) > -1 && !best_candiate) {
              // Can't do return false here, since we still need to iterate over
              // all list items to see if there is an exact match
              best_candiate = $(this);
            };
            
          };
          if(context.settings.isFilter && text.search(current_value) > -1 && current_value != "")
      	  {
          	 $(this).show();
          	
      	  }else if(context.settings.isFilter)
      	  {
      		 $(this).hide();
      	  }
        }
      
      );
      
      if(best_candiate && !value_found) {
        context.clearSelectedListItem();
        context.selectListItem(best_candiate);
        context.scrollToListItem(best_candiate);
      }else if(!best_candiate && !value_found) {
        this.selectFirstListItem();
      };      
    },
    scrollToListItem: function(list_item) {
      if(this.list_height) {
        this.wrapper.scrollTop(list_item[0].offsetTop - (this.list_height / 2));
      };
    },
    hideList: function() {
      this.wrapper.hide();
      this.list_is_visible = false;
      if(this.settings.bg_iframe) {
        this.bg_iframe.hide();
      };
    },
    hideOtherLists: function() {
      for(var i = 0; i < instances.length; i++) {
        if(i != this.select.data('editable-selecter')) {
          instances[i].hideList();
        };
      };
    },
    positionElements: function() {
      var offset = this.text.offset();
      offset = { top: offset.top, left: offset.left };
      offset.top += this.text[0].offsetHeight;
      this.wrapper.css({top: offset.top +'px', left: offset.left +'px'});
      // Need to do this in order to get the list item height
      this.wrapper.css('visibility', 'hidden');
      this.wrapper.show();
      this.list_item_height = this.wrapper.find('li')[0] ? this.wrapper.find('li')[0].offsetHeight : 0;
      this.wrapper.css('visibility', 'visible');
      this.wrapper.hide();
    },
    setWidths: function() {
      // The text input has a right margin because of the background arrow image
      // so we need to remove that from the width
      this.select.show();
      var width = this.select.width() + 2 + 20;
      this.select.hide();
      var padding_right = parseInt(this.text.css('padding-right').replace(/px/, ''), 10);
      this.text.width(width - padding_right + 18);
      this.wrapper.width(width + 2 + 20);
      if(this.bg_iframe) {
        this.bg_iframe.width(width + 4 + 20);
      };
    },
    createBackgroundIframe: function() {
      var bg_iframe = $('<iframe frameborder="0" class="editable-select-iframe" src="about:blank;"></iframe>');
      $(document.body).append(bg_iframe);
      bg_iframe.width(this.select.width() + 2);
      bg_iframe.height(this.wrapper.height());
      bg_iframe.css({top: this.wrapper.css('top'), left: this.wrapper.css('left')});
      this.bg_iframe = bg_iframe;
    }
  };
})(jQuery);