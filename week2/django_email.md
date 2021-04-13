> Compare the write_message methods of the console-based and
> file-based backends. There is hidden coupling between them. What is
> the hidden coupling? What changes does this hidden coupling inhibit?
> How would you refactor them to eliminate it. 
> Hint: If your answer is related to inheritance, then you are likely
> noticing an instance of visible coupling, and are on the wrong
> track. 

`write_message` in the file-based backend assumes that
`self.stream` has already been initialized. The one in the
console-based one doesn't seem to.  This  means that
`write_messages` for the file-based backend always has to be
called after a call to `open`. This is not so for the console-based backend.

To eliminate this hidden dependency, I would give the file-based
backend its own stream at init time, there is no need to classes to
share private variables in this case. I would also not use
`self._stream` directly, and instead just use `open` to create the
stream. The code would look something like this:
```
def write_message(self, message, stream):
   stream.write(message.message().as_bytes() + b'\n')
   ...
   
def send_messages(self, email_messages):
   # acquire lock
   stream = self.open()
   ...
   for message in email_messages:
      self.write_message(message, stream)
   
```


> The send_messages methods of both the SMTP-based and console-based
> (and file-based, by inheritance) backends have a common notion of
> failing silently according to an option. # 
>    1. What is the essence of the "fail-silently" pattern? In other
> words, if I gave code where all identifiers were obfuscated, how
> would you identify code that implemented the "fail-silently"
> feature? Give your answer either as a very specific description of
> data- and control-flow to look for, or as a code skeleton. 


1. The essence of the `fail-silently` is to choose whether to bubble up
errors due to communications with external systems when opening up a
connection with those systems. It's not present
in backends to send messages to internal resources like memory, disk,
console but it is implemented in the SMTP backend, which talks to an
external server/resource. This option only seems to apply to the
`open, close, send_messages` methods. I would identify code that
implements this idea by looking at what the code did when encountering
an error on I/O operations. I would look for code that looks like:
```
def io_operation(...):
  try:
     # perform some I/O with external system
  except SomeExeption:
      raise 
```

>    2. What are the design decisions which are the same between the two
> backend's implementation of fail-silently, and how might a change to
> these decisions affect both implementations? Think about other
> policies for how the application should handle exceptions other than
> "fail at the top-level immediately for all exceptions" and "silently
> drop all exceptions." 

2. The design decisions which are the same are:
   - if there is any error on an email backend's connection
     (specifically opening via `open` or closing via `close`), then: 
     - an error will be returned by the program if `fail_silently` is
       set. 
     - Otherwise, no error is thrown, but processing of messages is stopped.
   - an email backend can send more than email message at a time
   - the backend will try to send emails one at a time. If an error
     happens while sending any email:
     - the whole operation will be aborted if `fail_silently` is set
       and an exeption will be raised
     - otherwise, sending emails stops, but no error is shown to the user
 
If our policy for exception-handling becomes "retry 1 time on
failure", then the code in all backends will have to change to reflect
this new policy. Other examples: fail only on specific errors

>    3. Sketch how to refactor the code to eliminate this hidden
> coupling. A successful solution should give code for "failing
> silently" that can be used in contexts unrelated to E-mail. (Hint:
> Use Python's with statement) 

Try to send messages.
If an exception occurs when doing so, exit then:
- let the user know if configured
- otherwise do not

```
#########################################
class FailureNotifier:
    # determine what to do
    fail_silently:bool = True
    log_exception:bool = False
    
    @contextmanager
    def handle_exception(self, exception: Exception):
        if not fail_silently:
            raise Exception
        if log_exception:
            logger.log(exception)

            
class FileEmailBackend:
    def send_messages(self,messages, action):
        try:
            ...
        except Exception as e:
            FailureNotifier().handle_exception(e)
        
        
########
## Alternate solution: use a decorator and use it in
## every backend's send_messages

class FileEmailBackend:
    @handle_exceptions
    def send_messages(self,messages, action):
        pass
        
def handle_exception(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            method(self, *args, **kwargs)
        except Exception as e:
            if not self.fail_silently:
                raise e
```

> The __init__ method of the file-based backend is complicated because
> of the impedance mismatch between the file path argument it accepts
> and the actual requirements on files. 
> What are the concrete restrictions it is placing on file paths? What
> are the underlying design decisions behind these restrictions? 

The restrictions are:
    - the path must be a string
    - the path must refer to a directory
    - if the path exists, it must be a directory
    - the directory must exist for reading later
    - the backend must have permission to write to the whole directory
    
The overall intent is to use a file itself as a connection that can be
opened, read and written to. In this backend, the connection that we
have to work with is a file. 

> What changes to the system's overall design or assumptions may change this code?

Some examples:  

> Sketch how to refactor this method to embed the design decisions identified in 3.1 directly into the code.

- The code that establishes all these restrictions could be put in its
own method. 

- The stream could be created directly to be used for writing
  later. 
  
- change the value of `self.stream` should be done explicitly, not
  through the obscure `kwargs['stream'] = None`
  
Here is some code that illustrates some of the changes above:
```
def __init__(self, *args, file_path=None, **kwargs):
    self.file_path = file_path
    try:
       validate_file_path(self.file_path)
    except ImproperlyConfigured ic:
        raise
        
    super().__init__(*args, **kwargs)
    self.stream = open(self._get_filename(), 'ab')
    
```


> Look at the __init__ and message methods of EmailMessage. Notice the
> different representations and handling of different E-mail headers
> such as from, bcc, to. 
>    Use decision tables to explain how the different headers are
> treated. Create two decision tables: one to explain how a header is
> handled when an initial value is given in the constructor, and one
> to explain when none is given. 

Decision table for headers with values:

| Conditions                 | to               | cc             | bcc            | reply-to       |
|----------------------------|------------------|----------------|----------------|----------------|
| to is a string             | TypeError        | -              | -              | -              |
| to is something else       | turn into a list | -              | -              | -              |
| cc is a string             | -                | TypeError      | -              | -              |
| cc is something else       | -                | turn into list | -              | -              |
| bcc                        | -                | -              | TypeError      | -              |
|  bcc is something else     | -                | -              | turn into list | -              |
|  reply-to is a string      | -                | -              | -              | TypeError      |
| reply-to is something else | -                | -              | -              | turn into list |


Decision table for headers with no values:

| Conditions      | to         | cc         | bcc        | reply-to   |
|-----------------|------------|------------|------------|------------|
| to is empty     | empty list | -          | -          | -          |
| cc is empty     |            | empty list | -          | -          |
| bcc is empty    | -          | -          | empty list | -          |
| reply-to empty | -          | -          | -          | empty list |

>    Suppose a new standard came out. It says that every E-mail must
>    have a "Reply-to" header. It also allows all recipients to be
>    tagged with a reason (e.g.: "CC: thanks:intro-er@example.com,
>    keeping-in-the-loop:my-boss@example.com"). What changes would
>    this require in the code?

The `reply_to` would now be a mandatory parameter in the constructor.

#The tag feature would force a change into the `sanitize_address` and
`split_addr` functions

>    Explain the design of the abstract concept of different kinds of
>    headers, i.e.: how would you explain what headers are, what
>    variations there are, and how they work to someone who had never
>    seen them before? How are these ideas expressed in the code? How
>    does this make the code complicated? 

The header fields of a message is used by an SMTP server to
communicates delivery parameters and information. When sending a
message, there is obviously the content of the message, but there is
also the information about the message itself such as:
- who is sending it
- on what date
- to what person
- etc

All this message metadata is what makes up email headers. Most header
fields are optional, except the FROM and DATE fields. 

The code represents all these header fields as disjointed fields that
are to be parsed/treated one by one. The same treatment is give to the
body and attachment parts of an email message

A better way would to have a `Headers` class that knows what to do
about header fields ,a `Body` class that deals with text and
attachment. The conceptually, we could write a class that unifies for
into a `EmailMessage`.

>    Sketch how to refactor this code based on the abstract design of headers.

```
class Headers:
    def __init__(self, from_field, date_field, **extra_fields):
        self.headers = {"from":self.format_field(from_field), "Date": self.format_field(date_field)}
        for k,v in extra_fields.items():
            self.headers[k] = self.format_field(v)
            
    def format_field(self,field):
        res = []
        if field:
            if isinstance(field, str):
                raise TypeError(..)
            res = list(field)
        return res
        
def Body:
    def __init__(self,text, content_subtype, encoding):
         self.msg = SafeMIMEText(text, content_subtype, encoding)
        
    def create_message(self):
        ...
        
    def _create_attachments(self):
        ...
        
class EmailMessage:
    def __init__(self, headers: Headers, body:Body):
        self.headers = headers
        self.body = body
        
    def message(self):
        msg = self.body.create_message()
        for header,value in self.headers.items():
            msg[header] = value
        return msg
```

> Bonus (optional): There are also at least two violations of the
> representable/valid principle (next week's lesson) in this code (at
> least one where it is possible to represent invalid states, and at
> least one where there are multiple states of EmailMessage that
> correspond to the same E-mail). Find them. How would you eliminate
> them? How would this simplify the code? 

