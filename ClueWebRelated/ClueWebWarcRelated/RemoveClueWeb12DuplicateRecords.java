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

public class RemoveClueWeb12DuplicateRecords {
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
  private HashSet<String> DuplicateRecords = new HashSet<String>(50000);

  /*
   * 
   */
  private void metaIOOpen(String fname) throws IOException {

    String cmd = "rm -rf " + fname;
    executeCommand(cmd,true);    
    System.out.println("Creating out file: " + fname);
    FileWriter outFileMeta = new FileWriter(fname, true);
    fileMeta = new PrintWriter(outFileMeta);   
  }

  /*
   * 
   */
  private void metaIOClose() throws IOException {
    fileMeta.close();    
  }
  /*
   * 
   */ /*
   * createDirectoryIfNeeded 
   */
  private void createDirectoryIfNeeded(String directoryName) {
    
    File theDir = new File(directoryName);
    // if the directory does not exist, create it
    if (!theDir.exists())
    {
      System.out.println("creating directory: " + directoryName);
      theDir.mkdirs();
    }
  }   /* end createDirectoryIfNeeded */
  /*
   * executeCommand - execute a bash command
   */
  public static String executeCommand(String command, boolean waitForResponse) {

    String response = "";
    ProcessBuilder pb = new ProcessBuilder("bash", "-c", command);
    pb.redirectErrorStream(true);

    try {
      Process shell = pb.start();
      if (waitForResponse) {
        // To capture output from the shell
        InputStream shellIn = shell.getInputStream();
        // Wait for the shell to finish and get the return code
        int shellExitStatus = shell.waitFor();
        if (shellExitStatus != 0) {
          System.out.println("Unexpected exit status in executeCommand. command: " + command + 
              ", status: "+ shellExitStatus);
        }
        response = convertStreamToStr(shellIn);
        shellIn.close();
      }
    }
    catch (IOException e) {
      System.out.println("Error occured while executing Linux command. Error Description: "  + e.getMessage());
    }
    catch (InterruptedException e) {
      System.out.println("Error occured while executing Linux command. Error Description: "  + e.getMessage());
    }
    return response;
  } /* end executeCommand */
  /*
   * executeCommand - used in executeCommand
   */
  public static String convertStreamToStr(InputStream is) throws IOException {

    if (is != null) {
      Writer writer = new StringWriter();

      char[] buf = new char[1024];
      try {
        Reader reader = new BufferedReader(new InputStreamReader(is,  "UTF-8"));
        int n;
        while ((n = reader.read(buf)) != -1) {
          writer.write(buf, 0, n);
        }
      } finally {
        is.close();
      }
      return writer.toString();
    }
    else {
      return "";
    }
  } /* end convertStreamToStr */
 
  /*
   * writebuffer - writes the buffer to the file.
   */
  public boolean writebuffer(String OutPathWarc) throws IOException {
    if (outputWarcFile == null) {
      String cmd = "rm -rf " + OutPathWarc;
      executeCommand(cmd,true);    

      GZIPOutputStream gzipOutStream = new GZIPOutputStream(new BufferedOutputStream(new FileOutputStream(new File(OutPathWarc), true)));      
      outputWarcFile = new DataOutputStream(gzipOutStream);
      if (outputWarcFile != null) {
        /* Put the header into a byte array*/
        HeaderRecord.setContentLength(HeaderRecord.getContent().length);
        // we need to increment by one to since the numbering begins at zero (0).
        HeaderRecord.addHeaderMetadata("WARC-Number-of-Documents", Integer.toString(Warc_Document_Counter));
        HeaderRecord.addHeaderMetadata("WARC-File-Length", Long.toString(currentByteBufferIndex));
        // remove any blank lines
        String s = HeaderRecord.getContentUTF8().replaceAll("(?m)^[ \t]*\r?\n", "");
        HeaderRecord.setContent(s.getBytes());
        int headersize= HeaderRecord.getTotalRecordLength();    
        // the + 6 is the 6 bytes we write below (3 x CRLF)
        HeaderRecord.addHeaderMetadata("WARC-File-Length", Long.toString(currentByteBufferIndex+headersize + 6));
        //write
        outputWarcFile.writeBytes(HeaderRecord.getHeaderString());
        writeCRLF(outputWarcFile, 1);
        int l = HeaderRecord.getByteContent().length;
        outputWarcFile.write(HeaderRecord.getByteContent(),0,l);
        writeCRLF(outputWarcFile, 2);
        outputWarcFile.flush();
        outputWarcFile.write(buffer, 0, currentByteBufferIndex);
        outputWarcFile.flush();
        outputWarcFile.close();
        outputWarcFile = null;
      } /* end if (outputWarcFile != null) */
    }  /* end if (outputWarcFile == null) */
    return true;      
  } /* end writebuffer */
  /*
   * writeCRLF - writes specified number of CRLF to file.
   */
  public void writeCRLF(DataOutputStream ofile, int num) throws IOException {
    for (int i=0; i<num;i++) {
      ofile.write(CRLF.getBytes(),0,CRLF.getBytes().length);
    }
  } /* End writeCRLF */

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

  /*
   *  process warc file 
   */
  public void removeDuplicates(String filename, String outputfile, String metafile ) throws IOException {

    Warc_Document_Counter = 0;  
    int recordCounts = 0; 
    String current_fullFilePath = outputfile;
    metaIOOpen(metafile);

    try {
      if (openWarcFileAndGetHeader(filename) ) {      
        // new file, start from zero
        while ( (record = WarcRecord.readNextWarcRecord(in)) != null) {
          recordCounts++;   
          RecordURI    = record.getHeaderMetadataItem("WARC-Target-URI");
          TrecID = record.getHeaderMetadataItem("WARC-TREC-ID");

          if ( !DuplicateRecords.contains(TrecID)) {
            Warc_Document_Counter++;
            copyRecordToBuffer();
          }
        }  // End warc record
        // write out new file
        if (Warc_Document_Counter != 0) {
          writebuffer(current_fullFilePath);
          closeInWarcFile();
        }
      }
    } 
    catch (IOException e) {
      System.err.println("Caught IOException: " + e.getMessage());        
    } 
    metaIOClose();

    g_Counts += Warc_Document_Counter;
    g_recordCounts += recordCounts;
    System.out.println("ClueWeb12 Records Created: " + Warc_Document_Counter +   " from " + recordCounts + " records.");

  } /* end processFile */

  /*
   *       
   */
  public void copyRecordToBuffer() throws IOException {

    fileMeta.println(TrecID + ", " + RecordURI );
    fileMeta.flush();

    int headerlength = record.getHeaderString().getBytes().length;
    int contentLength = record.getContent().length;
    // Do we have enough buffer space;
    int sizeNeeded = headerlength +  contentLength + (CRLFSize*3);
  
    if ((sizeNeeded+currentByteBufferIndex) > byteBufferMaxLength ) {
      // Okay make more room!
      int newsize = byteBufferMaxLength + byteBufferInc;
      byte[] nbuffer = new byte[newsize];
      System.arraycopy(buffer, 0, nbuffer, 0, currentByteBufferIndex);
      buffer = nbuffer; // JAVA is suppose to garbage collect, I hope it does!
      byteBufferMaxLength = newsize;
    }
    
    // write the record to the buffer
    System.arraycopy(record.getHeaderString().getBytes(), 0, buffer, currentByteBufferIndex, headerlength);
    currentByteBufferIndex += headerlength;
    System.arraycopy(CRLF.getBytes(), 0, buffer, currentByteBufferIndex, CRLFSize);
    currentByteBufferIndex += CRLFSize;
    System.arraycopy(record.getContent(), 0, buffer, currentByteBufferIndex, contentLength);  
    currentByteBufferIndex += contentLength;
    System.arraycopy(CRLF.getBytes(), 0, buffer, currentByteBufferIndex, CRLFSize);
    currentByteBufferIndex += CRLFSize;
    System.arraycopy(CRLF.getBytes(), 0, buffer, currentByteBufferIndex, CRLFSize);
    currentByteBufferIndex += CRLFSize;

  } /* end copyRecordToBuffer */

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
  /*
   * 
   */
  private void buildDuplicateDocList(String DuplicateDocIDListFilename) {
    try{
      System.out.println("Reading duplicate IDs from:" + DuplicateDocIDListFilename);
      FileInputStream fstream = new FileInputStream(DuplicateDocIDListFilename);
      DataInputStream in = new DataInputStream(fstream);
      BufferedReader br = new BufferedReader(new InputStreamReader(in));
      String strLine;
      DuplicateRecords.clear();
      //Read File Line By Line
      while ((strLine = br.readLine()) != null)   {
        DuplicateRecords.add(strLine);
      }
      in.close();
    } catch (Exception e){//Catch exception if any
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
      System.out.println("©2013 The Lemur Project.");
      System.out.println("http://www/lemurproject.org/");
      System.out.println("");
      System.out.println("RemoveClueWeb12DuplicateRecords -  version 1.0");
      System.out.println("");
      System.out.println("");
      System.out.println("usage:");
      System.out.println("java -jar RemoveClueWeb12DuplicateRecords.jar inputpath outputpath pathToDupRecords metaOutputDir");
      System.out.println("");
      System.out.println("inputpath  - path to the ClueWeb12 Segment directory to convert");
      System.out.println("outputpath - path to the output segement directory.");
      System.out.println("pathToDupRecords   -  path to the directory containing the files that have records to be removed");
      System.out.println("metaOutputDir   -  path to the toplevel directory to save the docid->url file");
      System.out.println("");
      System.out.println("Example:");
      System.out.println("java -jar ./RemoveClueWeb12DuplicateRecords.jar \\" );
      System.out.println("          /data1/ClueWeb12_Data/Disk1/ClueWeb12_01  \\");
      System.out.println("          /data1/ClueWeb12_Data_Nodups/Disk1/ClueWeb12_01 \\");
      System.out.println("          ./ClueWeb12DuplicateRecordsToRemove \\");
      System.out.println("          ./meta/Disk1/ClueWeb12_01");
      return;
    } 

    String pathtoSegment     = args[0];
    String outputDir         = args[1];
    String duplicateDocIdDir = args[2];
    String metaOutputDir     = args[3];
    
    RemoveClueWeb12DuplicateRecords createb13 = new RemoveClueWeb12DuplicateRecords();  
    createb13.createDirectoryIfNeeded(outputDir);
    createb13.createDirectoryIfNeeded(metaOutputDir);

    File directory = new File(pathtoSegment);
    if (directory.isDirectory()) {
      createb13.getFileListing(directory, createb13.g_dirListing);
      for ( File f : createb13.g_dirListing)  
      {  
        String inFilepath = f.getAbsolutePath();
        String d =  f.getAbsolutePath().replace(pathtoSegment, outputDir);
        if(f.isDirectory()) {
          createb13.createDirectoryIfNeeded(d);
        }
        if ( f.getName().endsWith("warc.gz") ) {
          String outfilePath =  inFilepath.replace(pathtoSegment, outputDir);
          System.out.println("Page processing on: " + inFilepath + "and saving to: " + outfilePath);
          System.out.flush();
          String fulldupfilename = duplicateDocIdDir + "/clueweb12-" + f.getName().replace(".warc.gz","dups.txt");
          String metafilename = metaOutputDir + "/clueweb12-" + f.getName().replace("warc.gz","meta.txt");
          File ff = new File(fulldupfilename);
          // If there are no duplicates just copy the file.
          if (!ff.exists()) {
            createb13.DuplicateRecords.clear();
            String cmd = "cp -p " + inFilepath + " " + outfilePath;
            executeCommand(cmd,true);   
            continue;
          }
          createb13.buildDuplicateDocList(fulldupfilename);
          try {
            createb13.removeDuplicates(inFilepath, outfilePath, metafilename);
          }
          catch (IOException e) {
            System.err.println("Caught IOException: " + e.getMessage());        
          } 
        } 
        else {
          System.out.println("Skipping - unexpected file extension " + inFilepath);
        }
      } // end for ( File f : p.g_dirListing) 
    } 
    System.out.println("");
    System.out.println("");
    System.out.println("Processing Competed.");
    System.out.println("Total ClueWeb12 Records Processed:   " + createb13.g_recordCounts );
    System.out.println("Total ClueWeb12 Records Created: " + createb13.g_Counts);
  } /* end main */

} /* End public class  */


