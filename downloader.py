import PySimpleGUI as sg
from pytube import YouTube as youtube
import webbrowser

def convertSeconds(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds) 

def loadVideo(video_object):
    window['-PROGRESSBAR-'].update(visible=False)
    window['-FILEPATH-'].update(visible=False)
    window['-VIDEOFRAME-'].update(visible=True)
    window['-AUDIOOFRAME-'].update(visible=True)
    window['-AUTHOR-'].update(video_object.author)
    window['-TITLE-'].update(video_object.title)
    window['-LENGTH-'].update(f'{convertSeconds(video_object.length)}')
    window['-VIEWS-'].update(video_object.views)
    window['-DESCRIPTION-'].update(video_object.description)
    window['-BESTSIZE-'].update(f'{round(video_object.streams.get_highest_resolution().filesize / 1048576, 2)} MB')
    window['-AUDIOSIZE-'].update(f'{round(video_object.streams.get_audio_only().filesize / 1048576, 2)} MB')

def onComplete(stream, filepath):
    print(f'download complete: {filepath}')
    window['-PROGRESSBAR-'].update(0)
    window['-PROGRESSBAR-'].update(visible=False)
    window['-FILEPATH-'].update(filepath)
    window['-FILEPATH-'].update(visible=True)

def progressCheck(stream, chunk, bytes_remaining):
    progress_amount = round(100 - (bytes_remaining / stream.filesize * 100))
    print(f'progress: {progress_amount}%')
    window['-PROGRESSBAR-'].update(progress_amount)


layout = [
    [sg.Text('Save to:'), sg.Text('', key='-SAVEFOLDER-'), sg.Button('Browse', key='-OPENFOLDER-')],
    [sg.Text('Video link:'), sg.Input(key='-LINK-'), sg.Button('Check', key='-LOAD-')],
    [sg.Text('Author:'), sg.Text('', key='-AUTHOR-')],
    [sg.Text('Title:'), sg.Text('', key='-TITLE-')],
    [sg.Text('Length:'), sg.Text('', key='-LENGTH-')],
    [sg.Text('Views:'), sg.Text('', key='-VIEWS-')],
    [
        sg.Text('Description'),
        sg.Multiline(
            '',
            key='-DESCRIPTION-',
            size=(60, 20),
            no_scrollbar=True,
            disabled=True
        )
    ],
    [
        sg.Frame('Best quality', [[
            sg.Text('', key='-BESTSIZE-'),
            sg.Button('Download', key='-BEST-')
        ]], key='-VIDEOFRAME-', visible=False),
        sg.Frame('Audio', [[
            sg.Text('', key='-AUDIOSIZE-'),
            sg.Button('Download', key='-AUDIO-')
        ]], key='-AUDIOOFRAME-', visible=False),
    ],
    [
        sg.Progress(100, size=(10, 10), expand_x=True, visible=False, key='-PROGRESSBAR-'),
        sg.Text('', key='-FILEPATH-', visible=False, enable_events=True),
    ]
]

window = sg.Window('Youtube downloader', layout)
download_path=''

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    
    if event == '-LOAD-':
        if values['-LINK-']:
            video_object = youtube(values['-LINK-'], on_progress_callback=progressCheck, on_complete_callback=onComplete)
            loadVideo(video_object)

    if event == '-BEST-':
        if not download_path:
            download_path = sg.popup_get_folder('Folder to save', no_window=True)
            print(download_path)
            window['-SAVEFOLDER-'].update(download_path)
        if download_path:
            window['-PROGRESSBAR-'].update(visible=True)
            video_object.streams.get_highest_resolution().download(download_path)
    if event == '-AUDIO-':
        if not download_path:
            download_path = sg.popup_get_folder('Folder to save', no_window=True)
            window['-SAVEFOLDER-'].update(download_path)
        if download_path:
            window['-PROGRESSBAR-'].update(visible=True)
            video_object.streams.get_highest_resolution().download(download_path)
    if event == '-OPENFOLDER-':
        download_path = sg.popup_get_folder('Folder to save', no_window=True)
        window['-SAVEFOLDER-'].update(download_path)
    if event == '-FILEPATH-':
        webbrowser.open('file:///' + download_path)


window.close()