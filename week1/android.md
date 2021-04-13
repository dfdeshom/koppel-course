
>Looper.prepareMainLooper is the method that determines that the
>currently executed thread is the main thread. Modify it to add ghost
>code to set isMainThread appropriately. (This should be a very small
>change.) 

```
public static void prepareMainLooper() {
107        prepare(false);
108        synchronized (Looper.class) {
109            if (sMainLooper != null) {
110                throw new IllegalStateException("The main Looper has already been prepared.");
111            }
112            sMainLooper = myLooper();
               isMainThread = true;
113        }
114    }
```

> isMainThread does not actually exist at runtime, but it is
> correlated with same program state that does. Write an invariant
> relating the value of isMainThread to physical state of the
> program. (Hint: Look up how Android engineers check if the current
> thread is the main thread.) 

Code to check for making sure the current thread is the main thread:
`Looper.myLooper() == Looper.getMainLooper()`. 

sMainLooper not null => isMainThread is true

>Instrumentation.java has many methods which ensure that they do not
>run on the main thread, while DynamicAnimation.java has many that
>ensure that they only run on the main thread. Find them. How do they
>do this check? Compare it to your answer in question 2. 

They check if the current `Looper`  is the main `Looper`, by comparing
>``Looper.myLooper() and Looper.getMainLooper()`.  

>Consider those "ensure" methods identified in Step 3. What
>preconditions and postconditions do these methods have relating to
>isMainThread? How about their callers? Can there be any transitive
>caller (e.g.: caller of a caller of a caller of a....) which doesn't
>have a precondition relating to isMainThread? (In other words, is it
>possible for the code to "learn" that it's running on the main
>thread.) 

Pre-conditions: isMainThread is false
Post-condition: isMainThread is true until animation has ended

Any calling code would have to check what the current global main
thread is

>Do the aforementioned methods in Instrumentation.java and
>DynamicAnimation.java "know" about the concept of a main thread? What
>do they know about how the main thread is implemented? 

They don't know the concept of a main thread, they just know there is
some thread they should either avoid or seek out.

> Suppose the physical code could read from ghost state. How would you
> refactor the code in Instrumentation.java and DynamicAnimation.java
> to do so, and in doing so reduce the knowledge of those two classes
> about the implementation details of Looper? 

```
private final void validateNotAppThread() {
1972        if (Looper.isMainthread == true) {
1973            throw new RuntimeException(
1974                "This method can not be called from the main application thread");
1975        }
1976    }
```

>How does the concept of having a main thread globally increase the
>complexity of Android apps? Think back to the semi-rigorous notions
>of complexity seen in the lesson on Hoare Logic. 

It's a state that you have to always keep in mind. Since it can also
change at any point in time, it requires careful tracking.
