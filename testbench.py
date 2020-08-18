#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Testbench
# Author: iracigt
# GNU Radio version: 3.8.0.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import kc2qol
import kc2qol, numpy
import numpy
from gnuradio import qtgui

class testbench(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Testbench")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Testbench")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "testbench")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.decim = decim = 1
        self.audio_samp_rate = audio_samp_rate = 40e3
        self.symbol_rate = symbol_rate = 20e3
        self.samp_rate = samp_rate = audio_samp_rate / decim
        self.sps = sps = float(samp_rate) / symbol_rate
        self.rolloff = rolloff = 0.2
        self.ntaps = ntaps = 31
        self.tx_taps_hex = tx_taps_hex = [119, -19, -111, 129, 21, -277, 199, 446, -619, -616, 1385, 760, -3014, -857, 10233, 17209, 10233, -857, -3014, 760, 1385, -616, -619, 446, 199, -277, 21, 129, -111, -19, 119]
        self.sym_per_arm = sym_per_arm = 8
        self.nfilts = nfilts = 16
        self.ideal_taps = ideal_taps = firdes.root_raised_cosine(int(sps), samp_rate, symbol_rate, rolloff, ntaps)
        self.thresh = thresh = 22
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(sps), rolloff, int(sym_per_arm*sps*nfilts))
        self.quant_taps = quant_taps = [round(2**15 * x) / 2**15 for x in ideal_taps]
        self.constel = constel = digital.constellation_calcdist([+0.70711 + +0.70711j, +1.0 + +0.0j, -1.0 + +0.0j, -0.70711 + -0.70711j, +0.0 + +1.0j, +0.70711 + -0.70711j, -0.70711 + +0.70711j, -0.0 + -1.0j], list(range(0,8)),
        8, 1).base()
        self.constel.gen_soft_dec_lut(8)
        self.act_taps = act_taps = [x * 2**-15 for x in tx_taps_hex]

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(0, 50)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_AUTO, qtgui.TRIG_SLOPE_POS, thresh, 512 / samp_rate , 0, "phase_est")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 0, 1, 2, 1)
        for r in range(0, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(0.1)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(True)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 3, 0, 1, 2)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0_0 = qtgui.const_sink_c(
            1024, #size
            "EVM Constellation", #name
            1 #number of inputs
        )
        self.qtgui_const_sink_x_0_0.set_update_time(0.001)
        self.qtgui_const_sink_x_0_0.set_y_axis(-1.5, 1.5)
        self.qtgui_const_sink_x_0_0.set_x_axis(-1.5, 1.5)
        self.qtgui_const_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0_0.enable_grid(True)
        self.qtgui_const_sink_x_0_0.enable_axis_labels(True)


        labels = ['Reclocked', 'Reference', 'Filtered', 'Raw', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "cyan", "yellow", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [2, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_0_win, 0, 0, 2, 1)
        for r in range(0, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.kc2qol_ldpc_decoder_fb_0 = kc2qol.ldpc_decoder_fb()
        self.kc2qol_dvbs2_pl_chunker_0_0 = kc2qol.dvbs2_pl_chunker(64800, pmt.intern('corr_est'), 90*3, numpy.float32)
        self.kc2qol_dvbs2_8psk_demod_0 = kc2qol.dvbs2_8psk_demod(None)
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_cc(
            digital.TED_MOD_MUELLER_AND_MULLER,
            sps,
            2*numpy.pi / 100 * 0.6,
            1.0,
            1.0,
            1.5,
            1,
            constel,
            digital.IR_MMSE_8TAP,
            128,
            [])
        self.digital_corr_est_cc_0 = digital.corr_est_cc([(0.70711+0.70711j), (0.70711-0.70711j), (-0.70711-0.70711j), (-0.70711+0.70711j), (0.70711+0.70711j), (-0.70711+0.70711j), (-0.70711-0.70711j), (0.70711-0.70711j), (0.70711+0.70711j), (0.70711-0.70711j), (0.70711+0.70711j), (-0.70711+0.70711j), (-0.70711-0.70711j), (-0.70711+0.70711j), (-0.70711-0.70711j), (0.70711-0.70711j), (-0.70711-0.70711j), (-0.70711+0.70711j), (-0.70711-0.70711j), (-0.70711+0.70711j), (0.70711+0.70711j), (-0.70711+0.70711j), (0.70711+0.70711j), (-0.70711+0.70711j), (-0.70711-0.70711j), (-0.70711+0.70711j)], 1, 1, thresh / 26, digital.THRESHOLD_ABSOLUTE)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_repack_bits_bb_0_0 = blocks.repack_bits_bb(1, 8, "", False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(1, 8, "", False, gr.GR_MSB_FIRST)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_not_xx_0_0 = blocks.not_bb()
        self.blocks_not_xx_0 = blocks.not_bb()
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_cc(2**-12)
        self.blocks_interleaved_short_to_complex_0 = blocks.interleaved_short_to_complex(False, False)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_short*1, '/Users/iracigt/Developer/DVB_hat/hdl/iq_bytes.bin', False, 0 * 21690 * 2, )
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_3_0 = blocks.file_sink(gr.sizeof_char*1, '/Users/iracigt/Desktop/packets_bin.bin', False)
        self.blocks_file_sink_3_0.set_unbuffered(True)
        self.blocks_file_sink_3 = blocks.file_sink(gr.sizeof_char*1, '/Users/iracigt/Desktop/packets_ldpc.bin', False)
        self.blocks_file_sink_3.set_unbuffered(True)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_cc(-3.8 * (1+1j))



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_interleaved_short_to_complex_0, 0))
        self.connect((self.blocks_interleaved_short_to_complex_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_not_xx_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.blocks_not_xx_0_0, 0), (self.blocks_repack_bits_bb_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.blocks_file_sink_3, 0))
        self.connect((self.blocks_repack_bits_bb_0_0, 0), (self.blocks_file_sink_3_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.digital_symbol_sync_xx_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_not_xx_0_0, 0))
        self.connect((self.digital_corr_est_cc_0, 1), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.digital_corr_est_cc_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.digital_corr_est_cc_0, 0), (self.kc2qol_dvbs2_8psk_demod_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.digital_corr_est_cc_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.qtgui_const_sink_x_0_0, 0))
        self.connect((self.kc2qol_dvbs2_8psk_demod_0, 0), (self.kc2qol_dvbs2_pl_chunker_0_0, 0))
        self.connect((self.kc2qol_dvbs2_pl_chunker_0_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.kc2qol_dvbs2_pl_chunker_0_0, 0), (self.kc2qol_ldpc_decoder_fb_0, 0))
        self.connect((self.kc2qol_ldpc_decoder_fb_0, 0), (self.blocks_not_xx_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "testbench")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim
        self.set_samp_rate(self.audio_samp_rate / self.decim)

    def get_audio_samp_rate(self):
        return self.audio_samp_rate

    def set_audio_samp_rate(self, audio_samp_rate):
        self.audio_samp_rate = audio_samp_rate
        self.set_samp_rate(self.audio_samp_rate / self.decim)

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate
        self.set_ideal_taps(firdes.root_raised_cosine(int(self.sps), self.samp_rate, self.symbol_rate, self.rolloff, self.ntaps))
        self.set_sps(float(self.samp_rate) / self.symbol_rate)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_ideal_taps(firdes.root_raised_cosine(int(self.sps), self.samp_rate, self.symbol_rate, self.rolloff, self.ntaps))
        self.set_sps(float(self.samp_rate) / self.symbol_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_AUTO, qtgui.TRIG_SLOPE_POS, self.thresh, 512 / self.samp_rate , 0, "phase_est")

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_ideal_taps(firdes.root_raised_cosine(int(self.sps), self.samp_rate, self.symbol_rate, self.rolloff, self.ntaps))
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.rolloff, int(self.sym_per_arm*self.sps*self.nfilts)))

    def get_rolloff(self):
        return self.rolloff

    def set_rolloff(self, rolloff):
        self.rolloff = rolloff
        self.set_ideal_taps(firdes.root_raised_cosine(int(self.sps), self.samp_rate, self.symbol_rate, self.rolloff, self.ntaps))
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.rolloff, int(self.sym_per_arm*self.sps*self.nfilts)))

    def get_ntaps(self):
        return self.ntaps

    def set_ntaps(self, ntaps):
        self.ntaps = ntaps
        self.set_ideal_taps(firdes.root_raised_cosine(int(self.sps), self.samp_rate, self.symbol_rate, self.rolloff, self.ntaps))

    def get_tx_taps_hex(self):
        return self.tx_taps_hex

    def set_tx_taps_hex(self, tx_taps_hex):
        self.tx_taps_hex = tx_taps_hex
        self.set_act_taps([x * 2**-15 for x in self.tx_taps_hex])

    def get_sym_per_arm(self):
        return self.sym_per_arm

    def set_sym_per_arm(self, sym_per_arm):
        self.sym_per_arm = sym_per_arm
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.rolloff, int(self.sym_per_arm*self.sps*self.nfilts)))

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.rolloff, int(self.sym_per_arm*self.sps*self.nfilts)))

    def get_ideal_taps(self):
        return self.ideal_taps

    def set_ideal_taps(self, ideal_taps):
        self.ideal_taps = ideal_taps
        self.set_quant_taps([round(2**15 * x) / 2**15 for x in self.ideal_taps])

    def get_thresh(self):
        return self.thresh

    def set_thresh(self, thresh):
        self.thresh = thresh
        self.digital_corr_est_cc_0.set_threshold(self.thresh / 26)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_AUTO, qtgui.TRIG_SLOPE_POS, self.thresh, 512 / self.samp_rate , 0, "phase_est")

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps

    def get_quant_taps(self):
        return self.quant_taps

    def set_quant_taps(self, quant_taps):
        self.quant_taps = quant_taps

    def get_constel(self):
        return self.constel

    def set_constel(self, constel):
        self.constel = constel

    def get_act_taps(self):
        return self.act_taps

    def set_act_taps(self, act_taps):
        self.act_taps = act_taps



def main(top_block_cls=testbench, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
