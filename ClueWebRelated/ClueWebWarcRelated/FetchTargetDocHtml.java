/*
 Lemur License Agreement

 Copyright (c) 2000-2013 The Lemur Project.  All rights reserved.

 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions
 are met:

 1. Redistributions of source code must retain the above copyright
 notice, this list of conditions and the following disclaimer.

 2. Redistributions in binary form must reproduce the above copyright
 notice, this list of conditions and the following disclaimer in
 the documentation and/or other materials provided with the
 distribution.

 3. The names "Lemur", "Indri", "University of Massachusetts" and
 "Carnegie Mellon" must not be used to endorse or promote products
 derived from this software without prior written permission. To
 obtain permission, contact license@lemurproject.org

 4. Products derived from this software may not be called "Lemur" or "Indri"
 nor may "Lemur" or "Indri" appear in their names without prior written
 permission of The Lemur Project. To obtain permission,
 contact license@lemurproject.org.

 THIS SOFTWARE IS PROVIDED BY THE LEMUR PROJECT AND OTHER
 CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
 BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
 FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 COPYRIGHT HOLDERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
 OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
 TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
 USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
 DAMAGE.

 */

/*
 *  March 24, 2013 - DAP
 *  
 *  The application was created to remove the duplicate records in the original ClueWeb12 
 *  dataset.
 *   
 */

import java.io.*;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.ArrayList;
import java.util.zip.GZIPInputStream;
import java.util.zip.GZIPOutputStream;
//

public class FetchTargetDocHtml {
  private GZIPInputStream gzipInStream;  
  private DataInputStream in;
  private WarcRecord HeaderRecord;
  private WarcRecord record;
  private DataOutputStream outputWarcFile = null;
  private int Warc_Document_Counter = 0;
  private int byteBufferMaxLength = 1288490000; //1.2GB  old 209715200; //200MB
  //if buffer needs to grow will grow by 100MB
  private int byteBufferInc = 104857600; //100MB 
  private byte[] buffer = new byte[byteBufferMaxLength];
  
  private int currentByteBufferIndex = 0;
  private int g_recordCounts = 0;
  private int g_Counts = 0;
  private String CRLF = "\r\n";
  private int CRLFSize = CRLF.getBytes().length;
  private List<File> g_dirListing = new ArrayList<File>();
  private String TrecID ="";
  private String RecordURI = "";
  private PrintWriter fileMeta; 
  private HashSet<String> TargetDocNo = new HashSet<String>(50000);
 
  /*
   * 
   */
  public boolean openWarcFileAndGetHeader(String InPathWarc) throws IOException {
    if (!InPathWarc.endsWith("warc.gz")) {
      System.out.println("InPathWarc does not end with warc.gz: filepath:" + InPathWarc); 
      return false;
    }
    /* setup IO */
    gzipInStream = new GZIPInputStream(new FileInputStream(InPathWarc));
    in = new DataInputStream(gzipInStream);

    HeaderRecord = WarcRecord.readNextWarcRecord(in);
    if (HeaderRecord == null) {
      System.out.println("results from first readNextWarcRecord is null: " + InPathWarc); 
      closeInWarcFile();
      return false;
    }

    return true;
  } /* end openWarcFileAndGetHeader */
  /*
   * 
   */
  public void closeInWarcFile() throws IOException {
    if (gzipInStream != null )
      gzipInStream.close();
    gzipInStream = null;
    currentByteBufferIndex=0;
  } /* end closeInWarcFile */


  public void writeTargetDoc(String filename, String outputfile) throws IOException {

	    String current_fullFilePath = outputfile;
	    PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(outputfile, false)
	    try {
	      if (openWarcFileAndGetHeader(filename) ) {      
	        // new file, start from zero
	        while ( (record = WarcRecord.readNextWarcRecord(in)) != null) {
	          recordCounts++;   
	          RecordURI = record.getHeaderMetadataItem("WARC-Target-URI");
	          TrecID = record.getHeaderMetadataItem("WARC-TREC-ID");

//	          if (TargetDocNo.contains(TrecID)) {
	        	  html = record.getContent();
	        	  html = html.replace("\n","\t");
	        	  out.println(TrecID + '\t' + html);
//	          }
	        }  // End warc record
	        // write out new file
	          closeInWarcFile();
	      }
	    } 
	    catch (IOException e) {
	      System.err.println("Caught IOException: " + e.getMessage());        
	    } 

	    System.out.println(filename + " processed"); 
	    out.close()
	  } /* end processFile */
  


  /*
   * getFileListing
   */
  private  void getFileListing(File dir, List<File> listing) {
    dir.setReadOnly();
    File[] files = dir.listFiles();
    Arrays.sort(files);
    for(int i = 0; i < files.length; i++) {
      listing.add(files[i]);
      if(files[i].isDirectory())
        getFileListing(files[i], listing);
    }
  } /* end getFileListing */


  
  private void buildTargetDocNoList(String TargetDocNoInName) {
	  try{
		  System.out.println("Reading DocNo from:" + TargetDocNoInName);
		  FileInputStream fstream = new FileInputStream(DuplicateDocIDListFilename);
	      DataInputStream in = new DataInputStream(fstream);
	      BufferedReader br = new BufferedReader(new InputStreamReader(in));
	      String StrLine;
	      TargetDocNo.clear();
	      while ((strLine = br.readLine()) != null) {
	    	TargetDocNo.add(strLine);  
	      }
	      in.close();
	      System.out.println("TargetDocNo built");
	  }catch (Exception e){//Catch exception if any
	      System.err.println("Error: " + e.getMessage());
    }
	  
  }
  
  /*
   *  Main - 
   *  Parameters:
   *  
   *  pathtoSegment - the full path to the segment of ClueWeb12 to convert to B13 data.
   *  outputpath    - the full path to the segment directory of the B13 data.
   */
  public static void main(String[] args) throws IOException, ClassNotFoundException {

    if  (args.length != 4) {
      System.out.println(args.length);

      System.out.println("");
      System.out.println("Fetch html of target DocNo -  version 1.0");
      System.out.println("");
      System.out.println("");
      System.out.println("usage:");
      System.out.println("java -jar FetchTargetDocHtml.jar inputfile outname targetDocNo");
      System.out.println("");
      System.out.println("inputfile  - path to the ClueWeb12 warc file");
      System.out.println("outname - path to the output file");
      System.out.println("targetDocNo   - DocNos to be fetched");
      System.out.println("");
      System.out.println("Example:");
      System.out.println("java -jar ./FetchTargetDocHtml.jar \\" );
      System.out.println("          /data1/ClueWeb12_Data/Disk1/ClueWeb12_01/.warc  \\");
      System.out.println("          outputname \\");
      System.out.println("          ./TargetDocNo");
      return;
    } 

    String WarcInName     = args[0];
    String OutName         = args[1];
    String TargetDocNoIn = args[2];
    
    FetchTargetDdocHtml createb13 = new FetchTargetDdocHtml();  

	created13.buildTargetDocNoList(TargetDocNoIn);
	created13.writeTargetDoc(WarcInName,OutName);

    System.out.println("");
    System.out.println("");
    System.out.println("Processing Competed.");
  } /* end main */

} /* End public class  */


