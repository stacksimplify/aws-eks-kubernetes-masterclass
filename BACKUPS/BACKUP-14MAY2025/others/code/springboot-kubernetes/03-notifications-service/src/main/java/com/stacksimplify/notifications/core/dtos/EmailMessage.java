package com.stacksimplify.notifications.core.dtos;

import java.util.List;

public class EmailMessage {

	private String subject;
	private String content;
	private String from;
	private List<String> toEmails;
	private List<String> ccEmails;
	private List<String> bccEmails;

	public String getSubject() {
		return subject;
	}

	public void setSubject(String subject) {
		this.subject = subject;
	}

	public String getContent() {
		return content;
	}

	public void setContent(String content) {
		this.content = content;
	}

	public String getFrom() {
		return from;
	}

	public void setFrom(String from) {
		this.from = from;
	}

	public List<String> getToEmails() {
		return toEmails;
	}

	public void setToEmails(List<String> toEmails) {
		this.toEmails = toEmails;
	}

	public List<String> getCcEmails() {
		return ccEmails;
	}

	public void setCcEmails(List<String> ccEmails) {
		this.ccEmails = ccEmails;
	}

	public List<String> getBccEmails() {
		return bccEmails;
	}

	public void setBccEmails(List<String> bccEmails) {
		this.bccEmails = bccEmails;
	}

}
