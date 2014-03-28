using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace Yaoi_Timer_1._3
{
    public partial class Form1 : Form
    {

        System.Diagnostics.Stopwatch sw = new System.Diagnostics.Stopwatch { };

        public Form1()
        {
            InitializeComponent();
            lblTimer.BackColor = Color.Transparent;
        }

        private void btnStart_Click(object sender, EventArgs e)
        {
            sw.Start();
            MainTimer.Enabled = true;
            lblTimer.ForeColor = System.Drawing.ColorTranslator.FromHtml("#000000");

        }

        private void btnPause_Click(object sender, EventArgs e)
        {
            sw.Stop();
            MainTimer.Stop();
            lblTimer.ForeColor = System.Drawing.ColorTranslator.FromHtml("#FFFF00");
        }

        private void bntSplit_Click(object sender, EventArgs e)
        {

        }

        private void btnStop_Click(object sender, EventArgs e)
        {
            var PAUSECOLOUR = "#FF0000";
            sw = System.Diagnostics.Stopwatch.StartNew();
            sw.Stop();
            MainTimer.Stop();
            lblTimer.ForeColor = System.Drawing.ColorTranslator.FromHtml(PAUSECOLOUR);
        }

        private void lblTimer_Click(object sender, EventArgs e)
        {

        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void MainTimer_Tick(object sender, EventArgs e)
        {
            int hrs = sw.Elapsed.Hours, mins = sw.Elapsed.Minutes, secs = sw.Elapsed.Seconds, mil = sw.Elapsed.Milliseconds;
            lblTimer.Text = hrs + ":";
            if (mins < 10)
                lblTimer.Text += "0" + mins + ":";
            else
                lblTimer.Text += mins + ":";
            if (secs < 10)
                lblTimer.Text += "0" + secs + ".";
            else
                lblTimer.Text += secs + ".";
            if (mil > 100)
                lblTimer.Text += mil;
            else
                lblTimer.Text += mil + "0";
        }

        private void btnRESET_Click(object sender, EventArgs e)
        {
            sw = System.Diagnostics.Stopwatch.StartNew();
            sw.Stop();
            MainTimer.Stop();
            lblTimer.Text = "0:00:00.000";
            lblTimer.ForeColor = System.Drawing.ColorTranslator.FromHtml("#000000");
            sw.Start();
            MainTimer.Start();
        }

    }
}
