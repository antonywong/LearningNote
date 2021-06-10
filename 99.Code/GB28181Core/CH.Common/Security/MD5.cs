using System;

namespace CH.Common.Security
{
    public class MD5
    {
        private string _PublicKey = "x2";
        public String PublicKey
        {
            get
            {
                return _PublicKey;
            }
            set
            {
                _PublicKey = value;
            }
        }


        public String Encrypt(string encryptString, string privateKeys)
        {
            System.Security.Cryptography.MD5CryptoServiceProvider x = new System.Security.Cryptography.MD5CryptoServiceProvider();
            byte[] bs = System.Text.Encoding.UTF8.GetBytes(encryptString);
            bs = x.ComputeHash(bs);
            System.Text.StringBuilder s = new System.Text.StringBuilder();
            foreach (byte b in bs)
            {
                s.Append(b.ToString(privateKeys).ToLower());
            }
            string password = s.ToString();
            return password;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="decryptString"></param>
        /// <param name="privateKeys"></param>
        /// <returns></returns>
        public String Decrypt(string decryptString, string privateKeys)
        {
            throw new NotImplementedException();
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="encryptString"></param>
        /// <returns></returns>
        public String Encrypt(string encryptString)
        {
            return Encrypt(encryptString, _PublicKey);
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="decryptString"></param>
        /// <returns></returns>
        public String Decrypt(string decryptString)
        {
            throw new NotImplementedException();
        }
    }
}
