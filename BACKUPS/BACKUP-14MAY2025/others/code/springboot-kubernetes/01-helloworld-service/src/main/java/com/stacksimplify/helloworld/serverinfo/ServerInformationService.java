package com.stacksimplify.helloworld.serverinfo;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class ServerInformationService {
	
	private static final String HOST_NAME = "HOSTNAME";

	private static final String INSTANCE_GUID = "LOCAL";

	@Value("${" + HOST_NAME + ":" + INSTANCE_GUID + "}")
	private String hostName;

	public String getServerInfo() {
		return hostName.substring(hostName.length()-5);
	}

}
