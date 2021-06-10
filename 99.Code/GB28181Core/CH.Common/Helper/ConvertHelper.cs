using System;
using System.Collections.Generic;

namespace CH.Common
{
    /// <summary>
    /// 
    /// </summary>
    public static class ConvertHelper
    {
        /// <summary>
        /// 
        /// </summary>
        public static Byte[] ToBytes(UInt16 input)
        {
            Byte[] result = new Byte[2];
            result[0] = (Byte)(input >> 8);
            result[1] = (Byte)input;
            return result;
        }

        /// <summary>
        /// 
        /// </summary>
        public static Int64 ToInt64(IList<Byte> input)
        {
            Int64 result = 0;
            for (Int32 i = 0; i < input.Count; i++)
            {
                Int64 temp = input[input.Count - 1 - i];
                result += temp << 8 * i;
            }
            return result;
        }
    }
}
