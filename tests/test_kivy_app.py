""" test ae.kivy_app portion. """
import os
import pytest
import shutil

# from kivy.core.window import Window
from kivy.base import stopTouchApp
from kivy.clock import Clock
from kivy.lang import Builder

from ae.gui_app import APP_STATE_SECTION_NAME, MainAppBase
from ae.kivy_app import (
    MAIN_KV_FILE_NAME, LOVE_VIBRATE_PATTERN, ERROR_VIBRATE_PATTERN, CRITICAL_VIBRATE_PATTERN, KivyMainApp, FrameworkApp)

TST_VAR = 'win_rectangle'
TST_VAL = (90, 60, 900, 600)

TST_DICT = {TST_VAR: TST_VAL}
def_ae_states = TST_DICT.copy()


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
        file_handle.write("\n".join(k + " = " + repr(v) for k, v in def_ae_states.items()))
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

    on_context_id_called = False
    on_font_size_called = False

    on_key_press_called = False
    on_key_release_called = False
    last_keys = ()

    def app_init(self, framework_app_class=FrameworkApp):
        """ called from MainAppBase """
        self.on_init_called = True
        self.app_title = "KivyAppTest Stub"
        super().app_init()

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

    def on_app_stop(self):
        """ called from KivyMainApp """
        self.on_stop_called = True

    def on_context_id(self):
        """ called from KivyMainApp """
        self.on_context_id_called = True

    def on_font_size(self):
        """ called from KivyMainApp """
        self.on_font_size_called = True

    def on_key_press(self, key, modifier):
        """ key press callback """
        self.on_key_press_called = True
        self.last_keys = key, modifier
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
    assert hasattr(MainAppBase, 'app_init')
    assert hasattr(MainAppBase, 'run_app')


SKIP_EXPRESSION = "'CI_PROJECT_ID' in os.environ"
skip_gitlab_ci = pytest.mark.skipif(SKIP_EXPRESSION, reason="headless gitlab CI python 3.6 image lacks window system")


@skip_gitlab_ci
class TestCallbacks:
    def test_setup_app_states(self, ini_file, restore_app_env):
        app = KivyMainApp(additional_cfg_files=(ini_file,))
        assert getattr(app, TST_VAR) == def_ae_states[TST_VAR]

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
        # assert app.framework_app.ae_states == def_ae_states

    def test_start(self, restore_app_env):
        app = KivyAppTest()
        assert not app.on_start_called
        Clock.schedule_once(app.framework_app.stop)
        app.run_app()
        assert app.on_start_called

    def test_context_id(self, restore_app_env):
        app = KivyAppTest()
        assert not app.on_context_id_called
        app.change_app_state('context_id', 'tstCtx')
        assert app.on_context_id_called

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
        Clock.schedule_once(app.framework_app.stop)
        app.run_app()
        assert app.on_stop_called

    def test_on_stop_with_stop_touch_app(self, restore_app_env):
        app = KivyAppTest()
        assert not app.on_stop_called
        Clock.schedule_once(lambda dt: stopTouchApp(), 0)
        app.run_app()
        assert app.on_stop_called


@skip_gitlab_ci
class TestAppState:
    def test_retrieve_app_states(self, ini_file, restore_app_env):
        app = KivyMainApp(additional_cfg_files=(ini_file,))
        assert app.get_var(TST_VAR, section=APP_STATE_SECTION_NAME) == TST_VAL
        assert app.retrieve_app_states() == TST_DICT

    def test_load_app_states(self, ini_file, restore_app_env):
        app = KivyMainApp(additional_cfg_files=(ini_file,))
        assert app.get_var(TST_VAR, section=APP_STATE_SECTION_NAME) == TST_VAL

        app.load_app_states()
        assert getattr(app, TST_VAR) == TST_VAL
        fas = app.framework_app.ae_states
        assert all(k in fas and v == fas[k] for k, v in TST_DICT.items())
        fas = app.retrieve_app_states()
        assert all(k in fas and v == fas[k] for k, v in TST_DICT.items())

    def test_setup_app_states(self, ini_file, restore_app_env):
        assert KivyMainApp.win_rectangle == MainAppBase.win_rectangle   # (0, 0, 800, 600)
        app = KivyMainApp(additional_cfg_files=(ini_file,))
        assert getattr(app, TST_VAR) == TST_VAL
        app.setup_app_states(TST_DICT)
        assert getattr(app, TST_VAR) == TST_VAL
        assert app.win_rectangle == def_ae_states[TST_VAR]

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
        fas = app.framework_app.ae_states
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
    def test_call_event_valid_method(self, ini_file, restore_app_env):
        app = KivyAppTest(additional_cfg_files=(ini_file,))
        assert not app.on_context_id_called
        assert app.call_event('on_context_id') is None
        assert app.on_context_id_called

    def test_call_event_return(self, ini_file, restore_app_env):
        app = KivyAppTest(additional_cfg_files=(ini_file,))
        assert not app.on_run_called
        Clock.schedule_once(app.framework_app.stop)
        assert app.call_event('run_app') == ""
        assert app.on_run_called

    def test_call_event_invalid_method(self, ini_file, restore_app_env):
        app = KivyMainApp(additional_cfg_files=(ini_file,))
        assert app.call_event('invalid_method_name') is None

    def test_main_kv_load(self, restore_app_env):
        try:
            with open(MAIN_KV_FILE_NAME, 'w') as fp:
                fp.write(MAIN_KV_LAYOUT)
            app = KivyMainApp()
            assert app.framework_app.kv_file == MAIN_KV_FILE_NAME
        finally:
            if os.path.exists(MAIN_KV_FILE_NAME):
                os.remove(MAIN_KV_FILE_NAME)

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
class TestContext:
    def test_set_context_with_send_event(self, ini_file, restore_app_env):
        app = KivyAppTest(additional_cfg_files=(ini_file,))
        assert len(app.context_path) == 0
        assert app.context_id == ""
        assert not app.on_context_id_called

        ctx1 = 'first_context'
        app.change_app_state('context_id', ctx1)
        assert len(app.context_path) == 0
        assert app.context_id == ctx1
        assert app.on_context_id_called

    def test_set_context_without_send_event(self, ini_file, restore_app_env):
        app = KivyAppTest(additional_cfg_files=(ini_file,))
        assert len(app.context_path) == 0
        assert app.context_id == ""
        assert not app.on_context_id_called

        ctx1 = 'first_context'
        app.change_app_state('context_id', ctx1, send_event=False)
        assert len(app.context_path) == 0
        assert app.context_id == ctx1
        assert not app.on_context_id_called

    def test_context_enter(self, ini_file, restore_app_env):
        app = KivyMainApp(additional_cfg_files=(ini_file,))
        assert len(app.context_path) == 0
        ctx1 = 'first_context'
        app.context_enter(ctx1)
        assert len(app.context_path) == 1
        assert app.context_path[0] == ctx1

    def test_context_enter_next_id(self, ini_file, restore_app_env):
        app = KivyMainApp(additional_cfg_files=(ini_file,))
        assert len(app.context_path) == 0
        assert app.context_id == ""
        ctx1 = 'first_context'
        ctx2 = '2nd_context'
        app.context_enter(ctx1, ctx2)
        assert len(app.context_path) == 1
        assert app.context_path[0] == ctx1
        assert app.context_id == ctx2

    def test_context_leave(self, ini_file, restore_app_env):
        app = KivyMainApp(additional_cfg_files=(ini_file,))
        ctx1 = 'first_context'
        app.context_enter(ctx1)

        app.context_leave()

        assert len(app.context_path) == 0
        assert app.context_id == ctx1

    def test_context_leave_next_id(self, ini_file, restore_app_env):
        app = KivyMainApp(additional_cfg_files=(ini_file,))
        ctx1 = 'first_context'
        ctx2 = '2nd_context'
        ctx3 = '3rd_context'
        app.context_enter(ctx1, ctx2)

        app.context_leave(next_context_id=ctx3)

        assert len(app.context_path) == 0
        assert app.context_id == ctx3


@skip_gitlab_ci
class TestKeyEvents:
    def test_key_press_text(self, restore_app_env):
        app = KivyAppTest()
        kbd = KeyboardStub()
        key_code = 32
        key_text = ' '
        modifiers = 0
        assert app.framework_app.on_key_down(kbd, key_code, None, key_text, modifiers)
        assert app.last_keys == (key_text, modifiers)

    def test_key_press_code(self, restore_app_env):
        app = KivyAppTest()
        kbd = KeyboardStub()
        key_code = 32
        key_text = ''
        modifiers = 0
        assert app.framework_app.on_key_down(kbd, key_code, None, key_text, modifiers)
        assert app.last_keys == (key_code, modifiers)

    def test_key_release(self, restore_app_env):
        app = KivyAppTest()
        kbd = KeyboardStub()
        key_code = 32
        assert app.framework_app.on_key_up(kbd, key_code, None)
        assert app.last_keys == (key_code, )
