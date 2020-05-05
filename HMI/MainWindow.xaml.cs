using NModbus;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Security;
using System.Net.Sockets;
using System.Security.Authentication;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Windows.Threading;

namespace HMI
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private EasyModbus.ModbusClient modbusClientPLC1;
        private EasyModbus.ModbusClient modbusClientPLC2;
        public MainWindow()
        {
            InitializeComponent();

            ClearTemperature.Click += new RoutedEventHandler(OnClearTempClick);
            ClearLevel.Click += new RoutedEventHandler(OnClearLevelClick);

            DispatcherTimer timer = new DispatcherTimer();
            timer.Interval = TimeSpan.FromSeconds(5);
            timer.Tick += UpdateTemperature;
            timer.Tick += UpdateLevels;
            timer.Start();

            //ClearTemperature.Click += GetData()


            //TcpClient client = new TcpClient("192.168.0.16", 5020);

            //using (SslStream sslStream = new SslStream(client.GetStream(), false, new RemoteCertificateValidationCallback(ValidateServerCertificate), null))
            //{
            //    //using (TcpClient client = new TcpClient("192.168.0.16", 5020))
            //    //{
            //    sslStream.AuthenticateAsClient("192.168.0.16", null, SslProtocols.Tls12, false);
            //    // This is where you read and send data

            //    var factory = new ModbusFactory();
            //    IModbusMaster master = factory.CreateMaster(client);

            //    // read five input values
            //    ushort startAddress = 1;
            //    ushort numInputs = 2;
            //    ushort[] inputs = master.ReadInputRegisters(1, startAddress, numInputs);

            //    for (int i = 0; i < numInputs; i++)
            //    {
            //        Console.WriteLine($"Input Registers {inputs[i]}");
            //    }
            //}
            //client.Close();

        }
        //public static bool ValidateServerCertificate(object sender, X509Certificate certificate, X509Chain chain, SslPolicyErrors sslPolicyErrors)
        //{
        //    return true;
        //}

        private int [] GetData(string slaveIP)
        {
            EasyModbus.ModbusClient modbusClientPLC = new EasyModbus.ModbusClient(slaveIP, 5020);

            modbusClientPLC.Connect();
            int[] serverResponse = modbusClientPLC.ReadInputRegisters(1, 2);

            return serverResponse;
        }

        private void UpdateTemperature(object sender, EventArgs e)
        {
            int[] temperatures = GetData("192.168.0.16");
            Fahrenheit.Content = "Fahrenheit: " + temperatures[0];
            Celsius.Content = "Celcius: " + temperatures[1];

            if (temperatures[0] > 194 || temperatures[1] > 90)
            {
                TemperatureWarning.Visibility = Visibility.Visible;
            }
            else
            {
                TemperatureWarning.Visibility = Visibility.Hidden;
            }
        }

        private void UpdateLevels(object sender, EventArgs e)
        {
            int[] levels = GetData("192.168.0.18");
            High.Content = "High: " + levels[0];
            Low.Content = "Low: " + levels[1];
        }

        private void OnClearTempClick(object sender, RoutedEventArgs e)
        {
            Fahrenheit.Content = "Fahrenheit: ";
            Celsius.Content = "Celsius: ";
        }

        
        private void OnClearLevelClick(object sender, RoutedEventArgs e)
        {
            High.Content = "High: ";
            Low.Content = "Low: ";
        }
    }
}
