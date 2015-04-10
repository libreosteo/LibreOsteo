function open_dropdown() {
        $('#user-toggle').parent().addClass('open');
      };

// Instance the tour
var tour = new Tour({
  template : "<div class='popover tour'>  <div class='arrow'></div>  <h3 class='popover-title'></h3>  <div class='popover-content'></div>  <div class='popover-navigation'>    <button class='btn btn-default' data-role='prev'>« Préc</button>    <span data-role='separator'>|</span>    <button class='btn btn-default' data-role='next'>Suiv »</button>    <button class='btn btn-default' data-role='end'>Terminer</button>  </div></div>",
  storage : false,
  onEnd : function(tour){
    $('#user-toggle').parent().off('hidden.bs.dropdown', open_dropdown);
    var menu = $('#user-toggle').next('.dropdown-menu');
      if (menu.is(":visible"))
      {
        $('#user-toggle').parent().removeClass('open');
      }
  },
});


function stepUserProfile() {
  return $.getJSON('/api/profiles/get_by_user').done(function(data)
  {
    if (!data.hasOwnProperty("adeli") || data.adeli == '') {
      tour.addStep(
      {
          element: "#user-profile",
          title: "Thérapeute",
          content: "Mettez à jour votre profil thérapeute. Le numéro ADELI est obligatoire pour les factures.",
          backdrop : false,
          placement: 'left',
          orphan : true,
          onShow : function(tour)
          {
            $('#user-toggle').parent().on('hidden.bs.dropdown', open_dropdown);
            $('#user-toggle').parent().addClass('open');
          }
      });
    }
  });
};

function stepOfficeSettings() {
  return $.getJSON('/api/settings').done(function(data){
  if (typeof data.currency === 'undefined' || data.currency == "" ){
    tour.addStep(
    {
      element: "#office-settings",
      title: "Paramétrer le cabinet",
      content: "Afin de pouvoir générer correctement les factures, il est nécessaire de mettre à jour les informations du cabinet.",
      backdrop : false,
      placement: 'left',
      orphan : true,
      onShow : function(tour)
      {
        $('#user-toggle').parent().on('hidden.bs.dropdown', open_dropdown);
        $('#user-toggle').parent().addClass('open');
      },
    });
  }
  });
};

function defineSteps() {
  stepUserProfile().then(stepOfficeSettings).then(function () {
    tour.init();
    if (tour.getStep(0)) {
      tour.start(true);
    }
  });
};

defineSteps();