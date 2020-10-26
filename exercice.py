#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mido
import json
import csv
import os
import time
import configparser
from copy import deepcopy

import inputs
import mido



NOTES_PER_OCTAVE = 12
DEFAULT_VELOCITY = 80

def build_note_dictionaries(note_names, add_octave_no=True):
	C0_MIDI_NO = 12 # Plus basse note sur les pianos est La 0, mais on va commencer à générer les noms sur Do 0

	midi_to_name = {}
	name_to_midi = {}
	# Pour chaque octave de 0 à 8 (inclus). On va générer tout l'octave 8, même si la dernière note du piano est Do 8
	for octave in range(8+1):
		# Pour chaque note de l'octave
		for note in range(NOTES_PER_OCTAVE):
			# Calculer le numéro MIDI de la note et ajouter aux deux dictionnaires
			midi_no = C0_MIDI_NO + octave * NOTES_PER_OCTAVE + note
			# Ajouter le numéro de l'octave au nom de la note si add_octave_no est vrai
			full_note_name = note_names[note] + (str(octave) if add_octave_no else "")
			midi_to_name[midi_no] = full_note_name
			# Garder les numéros de notes dans name_to_midi entre 0 et 11 si add_octave_no est faux
			name_to_midi[full_note_name] = midi_no if add_octave_no else midi_no % NOTES_PER_OCTAVE
	return midi_to_name, name_to_midi

def send_not_on(note_name, name_to_midi, midi_outputs)
	msg = mido.Message("note_on", note=name_to_midi[note_name], velocity=DEFAULT_VELOCITY)
	for o in midi_outputs:
		o.send(msg)

def send_not_of(note_name, name_to_midi, midi_outputs)
	msg = mido.Message("note_off", note=name_to_midi[note_name])
	for o in midi_outputs:
		o.send(msg)

def build_note_callbacks(note_name, name_to_midi, midi_outputs):
	# Construire des callbacks pour bouton appuyé et relâché
	def action_fn_pressed():
		send_not_on(note_name, name_to_midi, midi_outputs)
	def action_fn_released():
		send_not_of(note_name, name_to_midi, midi_outputs)
	return action_fn_pressed, action_fn_released

def build_chord_callbacks(chord, chord_notes, name_to_midi, midi_outputs):
	# Construire des callbacks pour bouton appuyé et relâché

	def action_fn_pressed():
		for note in chord()
		msg = mido.Message("note_on", note=name_to_midi[note_name], velocity = DEFAULT_VELOCITY)
		for o in midi_outputs:
			o.send(msg)
	def action_fn_released():
		msg = mido.Message("note_on", note=name_to_midi[note_name], velocity =  DEFAULT_VELOCITY)
		for o in midi_outputs:
			o.send(msg)

	return action_fn_pressed, action_fn_released

def build_custom_action_callbacks(action_name, custom_actions, midi_outputs):
	# Construire des callbacks pour bouton appuyé et relâché
	return pressed, released

def load_input_mappings(filename, name_to_midi, chord_notes, midi_outputs, custom_actions={}):
	config = configparser.ConfigParser()
	config.read(filename)
	gamepad_section = config["gamepad"]

	mappings = {}
	for gamepad_input in gamepad_section:
		action_name = gamepad_section[gamepad_input]
		# Construire des callbacks pour l'action appropriée et l'ajouter au mapping.
		if action_name in name_to_midi:
			press, released = build_note_callbacks(action_name, name_to_midi("DO4"), midi_outputs)
			mappings[gamepad_input] = {True: press, False: releaed}
	return mappings


def main():
	gamepad = inputs.devices.gamepads[0]
	midi_outputs = (mido.open_output("UM-ONE 3"), mido.open_output("UnPortMIDI 4"))
	midi_input = mido.open_input("UM-ONE 0")

	notes_data = json.looad(open("notes.json", "r", ecoding="utf-8"))
	note_names = notes_data["solfeggio_names"]
	note_names = {} # Charger du JSON
	midi_to_name, name_to_midi = build_note_dictionaries([]) # Charger du JSON
	chords = notes_data["chords"] # Charger du JSON

	def foo0(midi_outputs):
		print("henlo")
	def foo1(midi_outputs):
		print("k bye")
	custom_actions = {
		"foo": {True: foo0, False: foo1}
	}

	mappings = load_input_mappings("input.ini", name_to_midi, chords, midi_outputs)

	while True:
		for e in gamepad.read():
			# if e.ev_type not in ("Sync") and e.code not in ("ABS_X", "ABS_Y","ABS_RX", "ABS_RY"):
			# 	print(e.ev_type, e.code, e.state)
			btn = e.code.lower()
			pressed = bool(e.state)
			if btn in mappings:
				mappings[btn][pressed]()


if __name__ == "__main__":
	main()
