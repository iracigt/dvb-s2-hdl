#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
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
import sip
from gnuradio import analog
from gnuradio import blocks
import pmt
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import qtgui

class fir_siggen(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
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

        self.settings = Qt.QSettings("GNU Radio", "fir_siggen")

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
        self.tx_taps_hex = tx_taps_hex = [226, -36, -211, 246, 40, -527, 379, 850, -1179, -1172, 2637, 1447, -5739, -1633, 19484, 32767, 19484, -1633, -5739, 1447, 2637, -1172, -1179, 850, 379, -527, 40, 246, -211, -36, 226]
        self.tx_taps_exp = tx_taps_exp = [-0.001129150390625, -0.009796142578125, -0.018341064453125, -0.025115966796875, -0.028533935546875, -0.027191162109375, -0.020172119140625, -0.00714111328125, 0.01141357421875, 0.0343017578125, 0.0596923828125, 0.08526611328125, 0.108551025390625, 0.127197265625, 0.139251708984375, 0.143402099609375, 0.143402099609375, 0.139251708984375, 0.127197265625, 0.108551025390625, 0.08526611328125, 0.0596923828125, 0.0343017578125, 0.01141357421875, -0.00714111328125, -0.020172119140625, -0.027191162109375, -0.028533935546875, -0.025115966796875, -0.018341064453125, -0.009796142578125, -0.001129150390625]
        self.tx_taps = tx_taps = firdes.root_raised_cosine(1, 2, 1, 0.2, 31)
        self.samp_rate = samp_rate = 32000
        self.act_taps = act_taps = [x * 2**-15 for x in tx_taps_hex]

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            1024, #size
            "", #name
            1 #number of inputs
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(False)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_win)
        self.interp_fir_filter_xxx_0_0 = filter.interp_fir_filter_ccc(1, tx_taps_hex)
        self.interp_fir_filter_xxx_0_0.declare_sample_delay(0)
        self.blocks_stream_mux_0 = blocks.stream_mux(gr.sizeof_gr_complex*1, [1, 1])
        self.blocks_multiply_const_vxx_2 = blocks.multiply_const_cc(32)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_cc(2**-12)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(2**-8)
        self.blocks_interleaved_short_to_complex_0 = blocks.interleaved_short_to_complex(False, False)
        self.blocks_interleaved_char_to_complex_0 = blocks.interleaved_char_to_complex(False)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_short*1, '/Users/iracigt/Developer/DVB_hat/hdl/iq_bytes.bin', False, 0 * 21690 * 2, )
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_short*1, '/Users/iracigt/Developer/DVB_hat/hdl/fir_correct_u16.bin', False)
        self.blocks_file_sink_0_0.set_unbuffered(True)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, '/Users/iracigt/Developer/DVB_hat/hdl/fir_in_u8.bin', False)
        self.blocks_file_sink_0.set_unbuffered(True)
        self.blocks_complex_to_interleaved_short_0 = blocks.complex_to_interleaved_short(False)
        self.blocks_complex_to_interleaved_char_0 = blocks.complex_to_interleaved_char(False)
        self.blocks_add_const_vxx_0_0 = blocks.add_const_cc(-4 * (1+1j))
        self.blocks_add_const_vxx_0 = blocks.add_const_cc(64+64j)
        self.analog_const_source_x_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_stream_mux_0, 1))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_complex_to_interleaved_char_0, 0))
        self.connect((self.blocks_add_const_vxx_0_0, 0), (self.blocks_stream_mux_0, 0))
        self.connect((self.blocks_complex_to_interleaved_char_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_complex_to_interleaved_char_0, 0), (self.blocks_interleaved_char_to_complex_0, 0))
        self.connect((self.blocks_complex_to_interleaved_short_0, 0), (self.blocks_file_sink_0_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_interleaved_short_to_complex_0, 0))
        self.connect((self.blocks_interleaved_char_to_complex_0, 0), (self.interp_fir_filter_xxx_0_0, 0))
        self.connect((self.blocks_interleaved_short_to_complex_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_complex_to_interleaved_short_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_add_const_vxx_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_2, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_stream_mux_0, 0), (self.blocks_multiply_const_vxx_2, 0))
        self.connect((self.interp_fir_filter_xxx_0_0, 0), (self.blocks_multiply_const_vxx_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "fir_siggen")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_tx_taps_hex(self):
        return self.tx_taps_hex

    def set_tx_taps_hex(self, tx_taps_hex):
        self.tx_taps_hex = tx_taps_hex
        self.set_act_taps([x * 2**-15 for x in self.tx_taps_hex])
        self.interp_fir_filter_xxx_0_0.set_taps(self.tx_taps_hex)

    def get_tx_taps_exp(self):
        return self.tx_taps_exp

    def set_tx_taps_exp(self, tx_taps_exp):
        self.tx_taps_exp = tx_taps_exp

    def get_tx_taps(self):
        return self.tx_taps

    def set_tx_taps(self, tx_taps):
        self.tx_taps = tx_taps

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_act_taps(self):
        return self.act_taps

    def set_act_taps(self, act_taps):
        self.act_taps = act_taps



def main(top_block_cls=fir_siggen, options=None):

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
