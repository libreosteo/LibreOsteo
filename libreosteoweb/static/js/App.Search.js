var PatientFinder = Backbone.View.extend({

   render: function () {

      // Add some markup to attach the autocomplete to
      this.$el.html('<input id="search" type="text" placeholder="Search" class="form-control"/>');

      // Create the widget.  Route searches to a custom handler
      this.$('#search')
         .autocomplete({ source: $.proxy( this.findPatients, this), minLength: 2 });

      return this;
   },

   // Use the bound collection to perform the search.
   // The custom search function adds some caching to reduce the
   // amount of traffic.  Using the Deferred object, wait for the
   // response and then call the autocomplete's provided callback
   findPatients: function ( request, response ) {

      $.when( this.collection.search( request.term ) )
         .then(function ( data ) { response( _.map(data, function ( d ) { return { value: d.id, label: d.title + ' ('+ d.year +')' }; }) ); });

   },

   // We want to show the movie title but use the movie ID to
   // fetch the model from the collection and a trigger an event
   // so other processing can occur.
   events: {
      'autocompletefocus' :    'handleFindFocus',
      'autocompleteselect' :   'handleFindSelect'
   },

   handleFindFocus: function ( e, ui ) {

      return false;

   },

   handleFindSelect: function ( e, ui ) {

      var m = this.collection.get( ui.item.value );

      this.$('#search').val( ui.item.label );

      this.trigger(' finder:selected', m );

      return false;

   }

});