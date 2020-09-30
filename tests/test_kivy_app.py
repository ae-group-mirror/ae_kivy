""" test ae.kivy_app portion. """
import os
from typing import cast
from unittest.mock import MagicMock

import pytest
import shutil
from unittest import mock

from kivy.base import stopTouchApp
from kivy.clock import Clock
from kivy.lang import Builder, Observable
from kivy.properties import BooleanProperty
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget

from ae.core import DEBUG_LEVEL_DISABLED, DEBUG_LEVEL_ENABLED
from ae.i18n import default_language
from ae.gui_app import APP_STATE_SECTION_NAME, id_of_flow, flow_key, replace_flow_action, MainAppBase
from ae.kivy_app import (
    MAIN_KV_FILE_NAME, LOVE_VIBRATE_PATTERN, ERROR_VIBRATE_PATTERN, CRITICAL_VIBRATE_PATTERN,
    KivyMainApp, FrameworkApp, ensure_tap_kwargs_refs, get_txt)


TST_VAR = 'win_rectangle'
TST_VAL = (90, 60, 900, 600)

TST_DICT = {TST_VAR: TST_VAL}
def_app_states = TST_DICT.copy()


MAIN_KV_LAYOUT = '''
<Main@FloatLayout>:
'''
Builder.load_string(MAIN_KV_LAYOUT)


@pytest.fixture
def ini_file(restore_app_env):
    """ provide test config file """
    fn = 'tests/tst.ini'
    with open(fn, 'w') as file_handle:
        file_handle.write(f"[{APP_STATE_SECTION_NAME}]\n")
        file_handle.write("\n".join(k + " = " + repr(v) for k, v in def_app_states.items()))
    yield fn
    if os.path.exists(fn):      # some exception/error-check tests need to delete the INI
        os.remove(fn)


class KeyboardStub:
    """ stub to simulate keyboard instance for key events. """
    def __init__(self, **kwargs):
        self.command_keys = kwargs


class KivyAppTest(KivyMainApp):
    """ kivy main app test implementation """
    app_state_list: list
    app_state_bool: bool

    on_init_called = False
    on_pause_called = False
    on_resume_called = False
    on_run_called = False
    on_start_called = False
    on_stop_called = False

    on_flow_id_called = False
    on_font_size_called = False

    on_key_press_called = False
    on_key_release_called = False
    last_keys = ()

    def init_app(self, framework_app_class=FrameworkApp):
        """ called from MainAppBase """
        self.on_init_called = True
        self.app_title = "KivyAppTest Stub"
        return super().init_app(framework_app_class=framework_app_class)

    def run_app(self):
        """ called by test routine """
        self.on_run_called = True
        return super().run_app()

    # events

    def on_app_start(self):
        """ called from KivyMainApp """
        self.on_start_called = True

    def on_app_pause(self):
        """ called from KivyMainApp """
        self.on_pause_called = True

    def on_app_resume(self):
        """ called from KivyMainApp """
        self.on_resume_called = True

    def on_kivy_app_stop(self):
        """ called from KivyMainApp """
        self.on_stop_called = True

    def on_flow_id(self):
        """ called from KivyMainApp """
        self.on_flow_id_called = True

    def on_font_size(self):
        """ called from KivyMainApp """
        self.on_font_size_called = True

    def on_key_press(self, modifiers, key):
        """ key press callback """
        self.on_key_press_called = True
        self.last_keys = modifiers, key
        return True

    def on_key_release(self, key):
        """ key release callback """
        self.on_key_release_called = True
        self.last_keys = key,
        return True


# some basic constant tests (running also on github ci image, because pytest returns exit code 5 if all tests skip)
def test_vibrate_pattern_types():
    assert isinstance(LOVE_VIBRATE_PATTERN, tuple)
    assert isinstance(ERROR_VIBRATE_PATTERN, tuple)
    assert isinstance(CRITICAL_VIBRATE_PATTERN, tuple)


def test_kv_default_file_name():
    assert isinstance(MAIN_KV_FILE_NAME, str)


def test_main_app_class_abstracts():
    assert hasattr(MainAppBase, 'init_app')


def test_ensure_tap_kwargs_refs():
    kwargs = dict()
    wid = cast(Widget, object())  # create real Widget instance fails at gitlab-CI with "Unable to get a Window, abort."

    ensure_tap_kwargs_refs(kwargs, wid)
    assert 'tap_kwargs' in kwargs

    assert 'tap_widget' in kwargs['tap_kwargs']
    assert kwargs['tap_kwargs']['tap_widget'] is wid

    assert 'popup_kwargs' in kwargs['tap_kwargs']
    assert 'parent' in kwargs['tap_kwargs']['popup_kwargs']
    assert kwargs['tap_kwargs']['popup_kwargs']['parent'] is wid


SKIP_EXPRESSION = "'CI_PROJECT_ID' in os.environ"
skip_gitlab_ci = pytest.mark.skipif(SKIP_EXPRESSION, reason="headless gitlab CI python 3.6 image lacks window system")


@skip_gitlab_ci
class TestCallbacks:
    def test_setup_app_states(self, ini_file, restore_app_env):
        app = KivyMainApp(additional_cfg_files=(ini_file,))
        assert getattr(app, TST_VAR) == def_app_states[TST_VAR]

    def test_retrieve_app_states(self, restore_app_env):
        app = KivyMainApp()
        assert app.retrieve_app_states() == dict()

    def test_init(self, restore_app_env):
        app = KivyAppTest()
        assert app.on_init_called

    def test_run(self, ini_file, restore_app_env):
        app = KivyAppTest()
        assert app.framework_app
        assert not app.on_run_called
        Clock.schedule_once(app.framework_app.stop)
        app.run_app()
        assert app.on_run_called
        # assert app.framework_app.app_states == def_app_states

    def test_start(self, restore_app_env):
        app = KivyAppTest()
        assert not app.on_start_called
        Clock.schedule_once(app.framework_app.stop)
        app.run_app()
        assert app.on_start_called

    def test_flow_id(self, restore_app_env):
        app = KivyAppTest()
        assert not app.on_flow_id_called
        app.change_app_state('flow_id', id_of_flow('tst', 'flow'))
        assert app.on_flow_id_called

    def test_on_pause(self, restore_app_env):
        app = KivyAppTest()
        assert not app.on_pause_called
        # Clock.schedule_once(lambda dt: Window.do_pause())
        app.framework_app.dispatch('on_pause')
        # Clock.schedule_once(app.framework_app.stop)
        # Clock.schedule_once(lambda dt: stopTouchApp(), 0.9)
        # app.run_app()
        assert app.on_pause_called

    def test_on_resume(self, restore_app_env):
        app = KivyAppTest()
        assert not app.on_resume_called
        app.framework_app.dispatch('on_resume')
        Clock.schedule_once(app.framework_app.stop, 0.6)
        app.run_app()
        assert app.on_resume_called

    def test_on_stop(self, restore_app_env):
        app = KivyAppTest()
        assert not app.on_stop_called
        # Clock.schedule_once(app.stop_app)
        Clock.schedule_once(app.framework_app.stop)
        app.run_app()
        assert app.on_stop_called

    def test_on_stop_with_stop_touch_app(self, restore_app_env):
        app = KivyAppTest()
        assert not app.on_stop_called
        Clock.schedule_once(lambda dt: stopTouchApp())
        app.run_app()
        assert app.on_stop_called


@skip_gitlab_ci
class TestAppState:
    def test_retrieve_app_states(self, ini_file, restore_app_env):
        app = KivyMainApp(additional_cfg_files=(ini_file,))
        assert app.get_var(TST_VAR, section=APP_STATE_SECTION_NAME) == TST_VAL
        fas = app.retrieve_app_states()
        assert all(k in fas and v == fas[k] for k, v in TST_DICT.items())

    def test_load_app_states(self, ini_file, restore_app_env):
        app = KivyMainApp(additional_cfg_files=(ini_file,))
        assert app.get_var(TST_VAR, section=APP_STATE_SECTION_NAME) == TST_VAL

        app.load_app_states()
        assert getattr(app, TST_VAR) == TST_VAL
        fas = app.framework_app.app_states
        assert all(k in fas and v == fas[k] for k, v in TST_DICT.items())
        fas = app.retrieve_app_states()
        assert all(k in fas and v == fas[k] for k, v in TST_DICT.items())

    def test_setup_app_states(self, ini_file, restore_app_env):
        assert KivyMainApp.win_rectangle == MainAppBase.win_rectangle   # (0, 0, 800, 600)
        app = KivyMainApp(additional_cfg_files=(ini_file,))
        assert getattr(app, TST_VAR) == TST_VAL
        app.setup_app_states(TST_DICT)
        assert getattr(app, TST_VAR) == TST_VAL
        assert app.win_rectangle == def_app_states[TST_VAR]

    def test_change_app_state(self, ini_file, restore_app_env):
        app = KivyMainApp(additional_cfg_files=(ini_file,))
        assert app.save_app_states() == ""
        assert app.get_var(TST_VAR, section=APP_STATE_SECTION_NAME) == TST_VAL
        fas = app.retrieve_app_states()
        assert all(k in fas and v == fas[k] for k, v in TST_DICT.items())

        chg_val = 'ChangedVal'
        chg_dict = {TST_VAR: chg_val}
        app.change_app_state(TST_VAR, chg_val)

        assert getattr(app, TST_VAR) == chg_val
        fas = app.framework_app.app_states
        assert all(k in fas and v == fas[k] for k, v in chg_dict.items())
        fas = app.retrieve_app_states()
        assert all(k in fas and v == fas[k] for k, v in chg_dict.items())

        assert app.get_var(TST_VAR, section=APP_STATE_SECTION_NAME) == TST_VAL
        assert app.save_app_states() == ""
        assert app.get_var(TST_VAR, section=APP_STATE_SECTION_NAME) == chg_val

    def test_save_app_states(self, ini_file, restore_app_env):
        global TST_DICT
        app = KivyMainApp(additional_cfg_files=(ini_file,))
        old_dict = TST_DICT.copy()
        try:
            assert app.get_var(TST_VAR, section=APP_STATE_SECTION_NAME) == TST_VAL
            fas = app.retrieve_app_states()
            assert all(k in fas and v == fas[k] for k, v in TST_DICT.items())

            chg_val = 'ChangedVal'
            TST_DICT = {TST_VAR: chg_val}
            setattr(app, TST_VAR, chg_val)
            assert app.save_app_states() == ""
            assert app.get_var(TST_VAR, section=APP_STATE_SECTION_NAME) == chg_val
            fas = app.retrieve_app_states()
            assert all(k in fas and v == fas[k] for k, v in TST_DICT.items())
        finally:
            TST_DICT = old_dict

    def test_save_app_states_exception(self, ini_file, restore_app_env):
        app = KivyMainApp(additional_cfg_files=(ini_file,))
        os.remove(ini_file)
        assert app.save_app_states() != ""

    def test_set_font_size(self, ini_file, restore_app_env):
        app = KivyAppTest(additional_cfg_files=(ini_file,))
        assert app.font_size == 30.0
        assert not app.on_font_size_called

        font_size = 99.9
        app.change_app_state('font_size', font_size)
        assert app.font_size == font_size
        assert app.on_font_size_called


@skip_gitlab_ci
class TestHelperMethods:
    def test_call_method_valid_method(self, ini_file, restore_app_env):
        app = KivyAppTest(additional_cfg_files=(ini_file,))
        assert not app.on_flow_id_called
        assert app.call_method('on_flow_id') is None
        assert app.on_flow_id_called

    def test_call_method_return(self, ini_file, restore_app_env):
        app = KivyAppTest(additional_cfg_files=(ini_file,))
        assert not app.on_run_called
        Clock.schedule_once(app.framework_app.stop)
        app.run_app()
        assert app.on_run_called

    def test_call_method_invalid_method(self, ini_file, restore_app_env):
        app = KivyMainApp(additional_cfg_files=(ini_file,))
        assert app.call_method('invalid_method_name') is None

    def test_ensure_top_most_z_index(self, restore_app_env):
        app = KivyAppTest()
        app.framework_win = MagicMock()
        app.framework_win.children = list()
        app.framework_win.add_widget = lambda child: app.framework_win.children.insert(0, child)

        wid = MagicMock()
        app.framework_win.add_widget(wid)
        assert app.framework_win.children[0] == wid
        app.ensure_top_most_z_index(wid)
        assert app.framework_win.children[0] == wid

        wid2 = MagicMock()
        app.framework_win.add_widget(wid2)
        assert app.framework_win.children[0] != wid
        app.ensure_top_most_z_index(wid)
        assert app.framework_win.children[0] == wid

    def test_main_kv_load(self, restore_app_env):
        try:
            with open(MAIN_KV_FILE_NAME, 'w') as fp:
                fp.write(MAIN_KV_LAYOUT)
            app = KivyMainApp()
            assert app.framework_app.kv_file == MAIN_KV_FILE_NAME
        finally:
            if os.path.exists(MAIN_KV_FILE_NAME):
                os.remove(MAIN_KV_FILE_NAME)

    def test_mix_background_ink(self, restore_app_env):
        app = KivyMainApp()
        app.mix_background_ink()
        assert app.framework_app.mixed_back_ink[0] \
            == (app.flow_id_ink[0] + app.flow_path_ink[0] + app.selected_item_ink[0] + app.unselected_item_ink[0]) / 4.0
        assert app.framework_app.mixed_back_ink[1] \
            == (app.flow_id_ink[1] + app.flow_path_ink[1] + app.selected_item_ink[1] + app.unselected_item_ink[1]) / 4.0
        assert app.framework_app.mixed_back_ink[2] \
            == (app.flow_id_ink[2] + app.flow_path_ink[2] + app.selected_item_ink[2] + app.unselected_item_ink[2]) / 4.0
        assert app.framework_app.mixed_back_ink[3] \
            == (app.flow_id_ink[3] + app.flow_path_ink[3] + app.selected_item_ink[3] + app.unselected_item_ink[3]) / 4.0

    def test_play_beep(self, restore_app_env):
        app = KivyMainApp()
        assert app.play_beep() is None

    def test_play_sound_missing(self, restore_app_env):
        app = KivyMainApp()
        assert app.play_sound('tst') is None

    def test_play_sound_wav(self, restore_app_env):
        sound_dir = 'snd'
        sound_file = 'tst_snd_file'
        try:
            os.mkdir(sound_dir)
            shutil.copy(os.path.join('tests', 'tst.wav'), os.path.join(sound_dir, sound_file + '.wav'))
            app = KivyMainApp()
            assert app.play_sound(sound_file) is None
        finally:
            shutil.rmtree(sound_dir)

    def test_play_sound_invalid_wav(self, restore_app_env):
        sound_dir = 'snd'
        sound_file = 'tst_snd_file'
        try:
            os.mkdir(sound_dir)
            with open(os.path.join(sound_dir, sound_file + '.mp3'), 'w') as fp:
                fp.write('invalid sound file content')
            app = KivyMainApp()
            assert app.play_sound(sound_file) is None
        finally:
            shutil.rmtree(sound_dir)

    def test_play_vibrate(self, restore_app_env):
        app = KivyMainApp()
        assert app.play_vibrate() is None

    def test_play_vibrate_invalid_pattern(self, restore_app_env):
        app = KivyMainApp()
        assert app.play_vibrate(('invalid pattern', )) is None


@skip_gitlab_ci
class TestFlow:
    def test_flow_enter(self, restore_app_env):
        app = KivyAppTest()
        assert len(app.flow_path) == 0
        flow1 = id_of_flow('enter', 'first_flow')
        app.change_flow(flow1)
        assert len(app.flow_path) == 1
        assert app.flow_path[0] == flow1

    def test_flow_enter_next_id(self, restore_app_env):
        app = KivyAppTest()
        assert len(app.flow_path) == 0
        assert app.flow_id == ""
        flow1 = id_of_flow('enter', 'first_flow')
        flow2 = id_of_flow('action', '2nd_flow')
        app.change_flow(flow1, flow_id=flow2)
        assert len(app.flow_path) == 1
        assert app.flow_path[0] == flow1
        assert app.flow_id == flow2

    def test_flow_leave(self, restore_app_env):
        app = KivyAppTest()
        flow1 = id_of_flow('enter', 'first_flow', 'tst_key')
        app.change_flow(flow1)
        assert len(app.flow_path) == 1
        assert app.flow_path[0] == flow1
        assert app.flow_id == id_of_flow('', '')

        flow2 = id_of_flow('leave', 'first_flow', 'tst_key')
        app.change_flow(flow2)
        assert len(app.flow_path) == 0
        assert app.flow_id == replace_flow_action(flow1, 'focus')
        assert flow_key(app.flow_id) == 'tst_key'

    def test_flow_leave_next_id(self, restore_app_env):
        app = KivyAppTest()
        flow1 = id_of_flow('enter', 'first_flow', 'tst_key')
        flow2 = id_of_flow('action', '2nd_flow', 'tst_key2')
        flow3 = id_of_flow('leave', '3rd_flow')
        app.change_flow(flow1, flow_id=flow2)
        assert app.flow_id == flow2

        app.change_flow(flow3, flow_id=flow3)
        assert len(app.flow_path) == 0
        assert app.flow_id == flow3

    def test_set_flow_with_send_event(self, restore_app_env):
        app = KivyAppTest()
        assert len(app.flow_path) == 0
        assert app.flow_id == ""
        assert not app.on_flow_id_called

        flow1 = 'first_flow'
        app.change_app_state('flow_id', flow1)
        assert len(app.flow_path) == 0
        assert app.flow_id == flow1
        assert app.on_flow_id_called

    def test_set_flow_without_send_event(self, restore_app_env):
        app = KivyAppTest()
        assert len(app.flow_path) == 0
        assert app.flow_id == ""
        assert not app.on_flow_id_called

        flow1 = 'first_flow'
        app.change_app_state('flow_id', flow1, send_event=False)
        assert len(app.flow_path) == 0
        assert app.flow_id == flow1
        assert not app.on_flow_id_called


@skip_gitlab_ci
class TestEvents:
    def test_key_press_text(self, restore_app_env):
        app = KivyAppTest()
        kbd = KeyboardStub()
        key_code = 32
        key_text = 'y'
        modifiers = ["alt"]
        app.framework_app.key_press_from_kivy(kbd, key_code, None, key_text, modifiers)
        assert app.last_keys == (modifiers[0].capitalize(), key_text)

    def test_key_press_code(self, restore_app_env):
        app = KivyAppTest()
        kbd = KeyboardStub()
        key_code = 369
        key_text = ''
        modifiers = ["meta", "ctrl"]
        app.framework_app.key_press_from_kivy(kbd, key_code, None, key_text, modifiers)
        assert app.last_keys == ("CtrlMeta", str(key_code))

    def test_key_release(self, restore_app_env):
        app = KivyAppTest()
        kbd = KeyboardStub()
        key_code = 32
        app.framework_app.key_release_from_kivy(kbd, key_code, None)
        assert app.last_keys == (str(key_code), )

    def test_on_flow_widget_focused(self, restore_app_env):
        app = KivyAppTest()

        class Wid:
            """ test dummy """
            focus = False
            is_focusable = True

        wid = Wid()
        app.widget_by_flow_id = lambda flow_id: wid
        app.on_flow_widget_focused()
        assert wid.focus is True

    def test_on_kbd_input_mode_change(self, restore_app_env):
        app = KivyAppTest()
        old_mode = app.kbd_input_mode

        app.on_kbd_input_mode_change('', dict())
        assert app.kbd_input_mode == ''

        app.on_kbd_input_mode_change('any', dict())
        assert app.kbd_input_mode == 'any'

        # app.kbd_input_mode = old_mode
        assert app.on_kbd_input_mode_change(old_mode, dict())

    def test_on_light_theme_change(self, restore_app_env):
        app = KivyAppTest()

        app.on_light_theme_change('any', dict(light_theme=True))
        assert app.light_theme

        app.on_light_theme_change('any', dict(light_theme=False))
        assert not app.light_theme

    def test_on_user_preferences_open_enabling_debug(self, restore_app_env):
        app = KivyAppTest()

        app.debug_level = DEBUG_LEVEL_ENABLED
        assert app._debug_enable_clicks == 0
        assert not app.on_user_preferences_open('', dict())

        app.debug_level = DEBUG_LEVEL_DISABLED
        assert not app.on_user_preferences_open('', dict())
        assert not app.on_user_preferences_open('', dict())
        assert not app.on_user_preferences_open('', dict())
        assert app.debug_level == DEBUG_LEVEL_ENABLED

        app.debug_level = DEBUG_LEVEL_DISABLED
        assert not app.on_user_preferences_open('', dict())
        assert app._debug_enable_clicks == 1
        # using Clock.schedule_once(_delayed_test, 6.9) and the commented sub-function underneath -> get never executed:
        # def _delayed_test(dt: float):
        #     print("delayed test_on_user_preferences_open_enabling_debug after:", dt)
        #     assert app.debug_level == DEBUG_LEVEL_DISABLED
        #     assert app._debug_enable_clicks == 0
        started = Clock.time()
        while Clock.time() - started < 6.9:
            Clock.tick()
        assert app.debug_level == DEBUG_LEVEL_DISABLED
        assert app._debug_enable_clicks == 0

    def test_show_message(self, restore_app_env):
        def _chg_flow(flow_id, popup_kwargs):
            """ mock of app.change_flow """
            assert flow_id == id_of_flow('show', 'message')
            assert popup_kwargs['message'] == 'tst msg'
            assert popup_kwargs['title'] == 'tst tit'
        app = KivyAppTest()
        app.change_flow = _chg_flow
        app.show_message('tst msg', 'tst tit')

    def test_show_popup_basic(self, restore_app_env):
        app = KivyAppTest()
        called = False
        passed_pa = None

        class TestPopUp(Popup):
            """ popup test class """
            test_attr = BooleanProperty(False)

            @staticmethod
            def open(parent):
                """ open popup method """
                nonlocal called, passed_pa
                called = True
                passed_pa = parent

        # noinspection PyTypeChecker
        popup = app.show_popup(TestPopUp, test_attr=True)
        assert called
        assert hasattr(popup, 'test_attr')
        assert popup.test_attr is True

        # noinspection PyTypeChecker
        app.show_popup(TestPopUp, parent=popup, test_attr=True)
        assert passed_pa == popup

        assert hasattr(popup, 'close')

    @mock.patch('ae.kivy_app.sys_platform', return_value='android')
    def test_show_popup_like_android(self, restore_app_env):
        app = KivyAppTest()
        called = False
        passed_pa = None

        class TestPopUp(Popup):
            """ popup test class """
            test_attr = BooleanProperty(False)

            @staticmethod
            def open(parent):
                """ open popup method """
                nonlocal called, passed_pa
                called = True
                passed_pa = parent

        # noinspection PyTypeChecker
        popup = app.show_popup(TestPopUp, test_attr=True)
        assert called
        assert hasattr(popup, 'test_attr')
        assert popup.test_attr is True

        # noinspection PyTypeChecker
        app.show_popup(TestPopUp, parent=popup, test_attr=True)
        assert passed_pa == popup

        assert hasattr(popup, 'close')


called_bound = False


def bound(*_args, **_kwargs):
    """ bound test func """
    global called_bound
    called_bound = True


@skip_gitlab_ci
class TestI18N:
    def test_get_txt_instance(self):
        assert callable(get_txt)
        assert hasattr(get_txt, 'switch_lang')
        assert isinstance(get_txt, Observable)

    def test_binding(self):
        assert not get_txt.observers
        get_txt.fbind('_', bound)
        assert len(get_txt.observers) == 1

        get_txt.fbind('any', bound)
        assert len(get_txt.observers) == 1

    def test_unbinding(self):
        assert len(get_txt.observers) == 1      # from last test method
        get_txt.funbind('_', bound)
        assert not get_txt.observers

        get_txt.funbind('any', bound)
        assert not get_txt.observers

    def test_switch_lang(self):
        old_lang = default_language()
        get_txt.switch_lang('xx')
        assert default_language() == 'xx'
        default_language(old_lang)

    def test_translate(self):
        assert get_txt("text to translate") == "text to translate"

    def test_translate_with_count(self):
        assert get_txt("text with {count} to translate", count=69) == "text with 69 to translate"

    def test_update(self):
        get_txt.fbind('_', bound, ('arg0', ))
        assert not called_bound
        get_txt.switch_lang('yy')
        assert called_bound

    def test_on_lang_code_change(self, restore_app_env):
        app = KivyAppTest()

        app.on_lang_code_change('zz', dict())
        assert default_language() == 'zz'
