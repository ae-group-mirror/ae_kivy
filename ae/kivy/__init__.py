"""
core application classes and widgets for GUIApp-conform Kivy apps
=================================================================

this ae portion is providing additional :ref:`config-variables`, some useful constants, behaviors ande widgets
to provide enhanced functionality, multilingual context-sensitive help, user onboarding, product tours, walkthroughs
and tutorials built-into for your multi-platform apps.

this portion is composed of various modules. the enhanced widget classes are declared in the modules
:mod:`~ae.kivy.widgets` and :mod:`~ae.kivy.tours`, the behavior classes in :mod:`~ae.kivy.behaviors`,
the two application classes (:class:`~ae.kivy.app.FrameworkApp` and :class:`~ae.kivy.app.KivyMainApp`)
in :mod:`~ae.kivy.app` and the internationalization (i18n) wrapper (:func:`~ae.kivy.i18n.get_txt`)
in :mod:`~ae.kivy.i18n`.


kivy app constants and config variables
---------------------------------------

all the :ref:`config-variables` and app constants inherited from the base app classes are available.

.. hint::
    please see the documentation of the namespace portions/modules :mod:`ae.console` and :mod:`ae.gui_app` for more
    detailed information on all the inherited :ref:`config-variables`, :ref:`config-options`, :ref:`config-files` and
    :ref:`app-state-constants`.

the additional :ref:`config-variables` `win_min_width` and `win_min_height`, added by this portion, you can optionally
restrict the minimum size of the kivy main window of your app. their default values are set on app startup in the method
:meth:`~ae.kivy.app.KivyMainApp.on_app_start`.

more constants provided by this portion are in the constant declaration section of the :mod:`~ae.kivy.widgets` module.


widget classes
--------------

the widgets provided by this portion are based on the kivy widgets and are respecting the :ref:`app-state-variables`
specifying the desired app style (dark or light) and font size. most of them also change automatically the
:ref:`application flow`.

the following widgets provided by this portion will be registered in the kivy widget class maps by importing this module
to be available for your app:

* :class:`~ae.kivy.widgets.AppStateSlider`: extended version of :class:`~kivy.uix.slider.Slider`, changing the value of
  :ref:`app-state-variables`.
* :class:`~ae.kivy.widgets.FlowButton`: button to change the application flow.
* :class:`~ae.kivy.widgets.FlowDropDown`: attachable menu-like popup, based on :class:`~kivy.uix.dropdown.DropDown`.
* :class:`~ae.kivy.widgets.FlowInput`: dynamic kivy widget based on :class:`~kivy.uix.textinput.TextInput` with
  application flow support.
* :class:`~ae.kivy.widgets.FlowPopup`: dynamic auto-content-sizing popup to query user input or to show messages.
* :class:`~ae.kivy.widgets.FlowSelector`: attachable popup used for dynamic elliptic auto-spreading menus and toolbars.
* :class:`~ae.kivy.widgets.FlowToggler`: toggle button based on :class:`~ae.kivy.widgets.ImageLabel` and
  :class:`~kivy.uix.behaviors.ToggleButtonBehavior` to change the application flow or any flag or application state.
* :class:`~ae.kivy.widgets.HelpToggler` is a toggle button widget that switches the app's help and tour mode on and off.
* :class:`~ae.kivy.widgets.ImageLabel`: dynamic kivy widget extending the Kivy :class:`~kivy.uix.label.Label` widget
  with an image.
* :class:`~ae.kivy.widgets.MessageShowPopup`: simple message box widget based on :class:`~ae.kivy.widgets.FlowPopup`.
* :class:`~ae.kivy.widgets.OptionalButton`: dynamic kivy widget based on :class:`~ae.kivy.widgets.FlowButton`
  which can be dynamically hidden.
* :class:`~ae.kivy.widgets.ShortenedButton`: dynamic kivy widget based on :class:`~ae.kivy.widgets.FlowButton`
  shortening the button text.
* :class:`~ae.kivy.widgets.Tooltip` displays text blocks that are automatically positioned next to any
  widget to providing e.g. i18n context help texts or app tour/onboarding info.
* :class:`~ae.kivy.widgets.UserNameEditorPopup`: popup window used e.g. to enter new user, finally registered in the
  app config files.


behavior classes
----------------

* :class:`~ae.kivy.behaviors.ModalBehavior` is a generic mix-in class that provides modal behavior to any container
  widget.
* :class:`~ae.kivy.behaviors.HelpBehavior` extends and prepares any Kivy widget to show an
  individual help text for it.
* :class:`~ae.kivy.behaviors.TouchableBehavior`: extends toggle-/touch-behavior of
  :class:`~kivy.uix.behaviors.ButtonBehavior`.


mixing-in modal behavior
^^^^^^^^^^^^^^^^^^^^^^^^

to convert a container widget into a modal dialog, add the :class:`~ae.kivy.behaviors.ModalBehavior` mix-in class,
provided by this ae namespace portion.

the following code snippet demonstrates a typical implementation::

    class MyContainer(ModalBehavior, BoxLayout):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        def open(self):
            self.activate_esc_key_close()
            self.activate_modal()

        def close(self):
            self.deactivate_esc_key_close()
            self.deactivate_modal()


calling the method :meth:`~ae.kivy.behavior.ModalBehavior.activate_esc_key_close` in the `open` method of a container
class allows the user to close the popup by pressing the Escape key (or Back on Android). this optional feature can
be reverted by calling the :meth:`~ae.kivy.behavior.ModalBehavior.deactivate_esc_key_close` method in your
`close` method.

to additionally activate the modal mode call the method :meth:`~ae.kivy.behavior.ModalBehavior.activate_modal`.
the modal mode can be deactivated by calling the :meth:`~ae.kivy.behavior.ModalBehavior.deactivate_modal` method.

all touch, mouse and keyboard user interactions will be consumed or filtered after activating the modal mode. therefore
it is recommended to also visually change the GUI while in the modal mode, which has to be implemented by the mixing-in
container widget.

.. hint::
    usage examples of the :class:`~ae.kivy.behavior.ModalBehavior` mix-in are e.g. the classes :class:`TourOverlay` and
    :class:`~ae.kivy_app.FlowPopup`.


application classes
-------------------

the class :class:`~ae.kivy.app.KivyMainApp` is implementing a main app class that is reducing the amount of
code needed to create a Python application based on the `kivy framework <https://kivy.org>`_.

:class:`~ae.kivy.app.KivyMainApp` is based on the following classes:

    * the abstract base class :class:`~ae.gui_app.MainAppBase` which adds :ref:`application status`,
      :ref:`app-state-variables`, :ref:`app-state-constants`, :ref:`application flow` and :ref:`application events`.
    * :class:`~ae.console.ConsoleApp` is adding :ref:`config-files`, :ref:`config-variables` and :ref:`config-options`.
    * :class:`~ae.core.AppBase` is adding :ref:`application logging` and :ref:`application debugging`.

this namespace portion is also encapsulating the :class:`Kivy App class <kivy.app.App>` within the
:class:`~ae.kivy.app.FrameworkApp` class. this Kivy app class instance can be directly accessed from the
main app class instance via the :attr:`~ae.gui_app.MainAppBase.framework_app` attribute.


kivy application events
^^^^^^^^^^^^^^^^^^^^^^^

this portion is firing :ref:`application events` additional to the ones provided by :class:`~ae.gui_app.MainAppBase` by
redirecting events of Kivy's :class:`~kivy.app.App` class (the Kivy event/callback-method name is given in brackets).
these framework app events get fired after :meth:`~ae.gui_app.MainAppBase.on_app_run` in the following order:

    * on_app_build (kivy.app.App.build, after the main kv file get loaded).
    * on_app_built (kivy.app.App.build, after the root widget get build).
    * on_app_started (kivy.app.App.on_start)
    * on_app_pause (kivy.app.App.on_pause)
    * on_app_resume (kivy.app.App.on_resume)
    * on_app_stopped (kivy.app.App.on_stop)


i18n support
------------

the i18n module :mod:`~ae.kivy.i18n` is adding translatable f-strings to the python and kv code of your app
via the helper function :func:`~ae.kivy.i18n.get_txt` and the :class:`~ae.kivy.i18n._GetTextBinder` class.


generic widget to display help and tour texts
---------------------------------------------

the tooltip widget class :class:`~ae.kivy.widgets.Tooltip` is targeting any widget by pointing with an arrow to it. the
position and size of this widget gets automatically calculated from the targeted widget position and size and the
tooltip text size. and if the screen/window size is not big enough then the tooltip texts get scrollable.

.. hint::
    use cases of the class :class:`~ae.kivy.widgets.Tooltip` are e.g. the help texts prepared and displayed by the
    method :meth:`~ae.gui_help.HelpAppBase.help_display` as well as the "explaining widget" tooltips in an app tour.


help behaviour mixin
^^^^^^^^^^^^^^^^^^^^

to show a i18n translatable help text for a Kivy widget create either a subclass of the widget. the following example
allows to attach a help text to a Kivy :class:`~kivy.uix.button.Button`::

    from kivy.uix.button import Button
    from ae.kivy_help import HelpBehavior

    class ButtonWithHelpText(HelpBehavior, Button):
        ...

alternatively you can archive this via the definition of a new kv-lang rule, like shown underneath::

    <ButtonWithHelpText@HelpBehavior+Button>

.. note::
    to automatically lock and mark the widget you want to add help texts for, this mixin class has to be specified
    as the first inheriting class in the class or rule declaration.


help activation and de-activation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

use the widget class :class:`~ae.kivy.widgets.HelpToggler` provided by this namespace portion in your app to toggle
the active state of the help mode.

.. hint::
    the :class:`~ae.kivy.widgets.HelpToggler` class is using the low-level touch events to prevent the dispatch of the
    Kivy events `on_press`, `on_release` and `on_dismiss` to allow to show help texts for opened dropdowns and popups.


animated app tours
------------------

the :mod:`~ae.kivy.tours` module does overlay or augment the app’s user interface with product tours, tutorials,
walkthroughs and user onboarding/welcome features.

the class :class:`~ae.kivy.tours.TourOverlay` is implementing an overlay layout widget to display the animations,
shaders, tour page texts, tooltip text and the navigation buttons of an active/running app tour.

the :class:`~ae.kivy.tours.AnimatedTourMixin` can be mixed-into a tour class that inherits from
:class:`~ae.gui_help.TourBase` to extend it with animation and glsl shader features.

the class :class:`~ae.kivy.tours.AnimatedOnboardingTour` is based on :class:`~ae.gui_help.OnboardingTour` and
:class:`~ae.kivy.tours.AnimatedTourMixin` to extend the generic app onboarding tour
class with animations. it provides a generic app onboarding tour that covers the core features, that can be easily
extended with app-specific tour pages.

to integrate a more app-specific onboarding tour into your app, simply declare a class with a name composed by the name
of your app (:attr:`~ae.gui_app.MainAppBase.app_name`) in camel-case, followed by the suffix `'OnboardingTour'`.


unit tests
----------

unit tests are currently still incomplete and need at least V 2.0 of OpenGL and the kivy framework installed.

.. note::
    unit tests are currently not passing at the gitlab CI because is failing to set up
    a properly running OpenGL graphics/window system on the python image that all ae portions are using.
"""


__version__ = '0.3.109'
